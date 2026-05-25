---
name: skill-api-realtime
description: Real-time communication patterns — WebSocket, Server-Sent Events (SSE), and long polling for web applications. Use when adding live updates, chat, notifications, collaborative editing, presence indicators, or any feature where the server pushes data to the client. For GraphQL subscriptions see skill-api-graphql; for REST endpoint design see skill-api-rest; for auth on WebSocket connections see skill-auth.
---

# Real-Time APIs — WebSocket, SSE, and Push Patterns

Real-time means the server decides when to send data, not the client. The choice between WebSocket, SSE, and polling depends on directionality, protocol needs, and infrastructure constraints.

## When to Activate

Use when:
- Adding live updates, notifications, or activity feeds
- Building chat, collaborative editing, or multiplayer features
- Implementing presence indicators ("user is typing", "3 online")
- Streaming large responses (AI text generation, log tailing)
- Choosing between WebSocket, SSE, and polling for a use case
- Adding reconnection, heartbeat, or auth to an existing real-time connection

**Trigger phrases:** "WebSocket", "SSE", "Server-Sent Events", "real-time", "live updates", "push notifications", "chat", "presence", "typing indicator", "streaming response", "long polling", "Socket.IO"

## When NOT to Use

| Situation | Use instead |
|---|---|
| GraphQL subscriptions (query-shaped push) | `skill-api-graphql` |
| REST endpoint design (request-response) | `skill-api-rest` |
| Auth for WebSocket connections | `skill-auth` (token pattern applies) |
| Scaling WebSocket across pods with Redis | `skill-devops` (infra) + this skill (application) |

## Iron Laws

1. **Authenticate on connect AND on each message.** A user's permissions can change mid-session — don't trust the initial handshake forever.
2. **Always implement reconnection with backoff.** Networks drop. Tabs sleep. Clients must reconnect automatically without flooding the server.
3. **Filter server-side, not client-side.** Don't broadcast every event to every client and let the browser discard. That's a privacy leak and a bandwidth waste.
4. **Heartbeat or die.** Without a ping/pong, you can't distinguish "connection is idle" from "connection is dead." Dead connections leak memory.

## Technology Decision Table

| Question | WebSocket | SSE | Long Polling |
|---|---|---|---|
| **Direction** | Bidirectional | Server → Client only | Server → Client (simulated) |
| **Protocol** | `ws://` / `wss://` | HTTP (`text/event-stream`) | HTTP |
| **Auto-reconnect** | Manual (must implement) | Built-in (browser handles) | Manual |
| **Binary data** | ✅ Yes | ❌ Text only | ❌ Text only |
| **HTTP/2 multiplexing** | ❌ Separate TCP connection | ✅ Shares connection | ✅ |
| **Proxy / CDN friendly** | ⚠️ Needs upgrade support | ✅ Standard HTTP | ✅ |
| **Browser support** | All modern browsers | All modern browsers | All browsers |
| **When to use** | Chat, collab editing, gaming, bidirectional | Notifications, feeds, AI streaming, dashboards | Legacy, simple polling with lower latency |

**Default choice:**
- Need bidirectional? → **WebSocket**
- Server-to-client only (notifications, feeds, streaming)? → **SSE**
- Can't use either (corporate proxy, legacy)? → **Long polling** as fallback

## WebSocket — Full Implementation

### Server (Node.js with `ws`)

```ts
import { WebSocketServer, WebSocket } from 'ws';
import { verifyToken } from './auth';

const wss = new WebSocketServer({ noServer: true });

// Authenticate during HTTP upgrade
server.on('upgrade', async (req, socket, head) => {
  try {
    const token = new URL(req.url!, `http://${req.headers.host}`).searchParams.get('token');
    const user = await verifyToken(token);
    wss.handleUpgrade(req, socket, head, (ws) => {
      (ws as any).user = user;
      wss.emit('connection', ws, req);
    });
  } catch {
    socket.write('HTTP/1.1 401 Unauthorized\r\n\r\n');
    socket.destroy();
  }
});

// Connection handling
wss.on('connection', (ws) => {
  const user = (ws as any).user;

  // Join user to their rooms/channels
  channels.join(user.id, ws);

  // Heartbeat — detect dead connections
  ws.isAlive = true;
  ws.on('pong', () => { ws.isAlive = true; });

  ws.on('message', (raw) => {
    try {
      const msg = JSON.parse(raw.toString());
      // Re-verify permission per message (Iron Law #1)
      if (!canAccess(user, msg.channel)) {
        ws.send(JSON.stringify({ type: 'error', code: 'FORBIDDEN' }));
        return;
      }
      handleMessage(user, msg);
    } catch {
      ws.send(JSON.stringify({ type: 'error', code: 'INVALID_MESSAGE' }));
    }
  });

  ws.on('close', () => {
    channels.leave(user.id);
  });
});

// Heartbeat interval — kill dead connections
setInterval(() => {
  wss.clients.forEach((ws) => {
    if (!ws.isAlive) return ws.terminate();
    ws.isAlive = false;
    ws.ping();
  });
}, 30_000);
```

### Client with reconnection

```ts
class ReconnectingWebSocket {
  private ws: WebSocket | null = null;
  private retries = 0;
  private maxRetries = 10;

  constructor(private url: string, private onMessage: (data: unknown) => void) {
    this.connect();
  }

  private connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      this.retries = 0;  // reset on successful connection
    };

    this.ws.onmessage = (event) => {
      this.onMessage(JSON.parse(event.data));
    };

    this.ws.onclose = (event) => {
      if (event.code === 1000) return;  // clean close, don't reconnect
      this.reconnect();
    };

    this.ws.onerror = () => {
      this.ws?.close();
    };
  }

  private reconnect() {
    if (this.retries >= this.maxRetries) return;
    const delay = Math.min(1000 * Math.pow(2, this.retries) + Math.random() * 500, 30_000);
    this.retries++;
    setTimeout(() => this.connect(), delay);
  }

  send(data: unknown) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  close() {
    this.ws?.close(1000);  // clean close code
  }
}
```

## Server-Sent Events (SSE)

### Server

```ts
// Express SSE endpoint
app.get('/api/events', authenticate, (req, res) => {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    Connection: 'keep-alive',
  });

  // Send initial data
  res.write(`data: ${JSON.stringify({ type: 'connected' })}\n\n`);

  // Subscribe to events for this user
  const handler = (event: unknown) => {
    res.write(`event: notification\ndata: ${JSON.stringify(event)}\n\n`);
  };
  eventBus.on(`user:${req.user.id}`, handler);

  // Heartbeat — keep connection alive through proxies
  const heartbeat = setInterval(() => {
    res.write(': heartbeat\n\n');  // comment line, ignored by EventSource
  }, 15_000);

  req.on('close', () => {
    clearInterval(heartbeat);
    eventBus.off(`user:${req.user.id}`, handler);
  });
});
```

### Client

```ts
const source = new EventSource('/api/events', {
  // Note: EventSource doesn't support custom headers — pass token in query
  // or use a polyfill that supports headers
});

source.addEventListener('notification', (event) => {
  const data = JSON.parse(event.data);
  showNotification(data);
});

source.onerror = () => {
  // Browser auto-reconnects with Last-Event-ID header
  // but you may want to handle prolonged failures
};
```

SSE advantages: auto-reconnect is built into the browser; `Last-Event-ID` header lets the server resume from where the client left off. SSE disadvantage: no custom headers (use cookies or query params for auth).

## Scaling Across Multiple Servers

Single-server `EventEmitter` won't fan out to clients on other pods. Use a pub/sub layer:

```ts
// Redis pub/sub for cross-server broadcast
import { createClient } from 'redis';

const pub = createClient({ url: process.env.REDIS_URL });
const sub = pub.duplicate();
await Promise.all([pub.connect(), sub.connect()]);

// Publish from any server
async function broadcast(channel: string, data: unknown) {
  await pub.publish(channel, JSON.stringify(data));
}

// Subscribe on each server — delivers to local WebSocket clients
await sub.subscribe('notifications', (message) => {
  const data = JSON.parse(message);
  localClients.get(data.userId)?.send(message);
});
```

| Tool | Best for |
|---|---|
| Redis pub/sub | Simple fan-out, ephemeral messages |
| NATS | High-throughput, lightweight, persistent queues |
| Kafka | Event sourcing, durable ordered streams |
| Socket.IO adapter (Redis) | Drop-in scaling for Socket.IO |

## Room / Channel Pattern

```ts
// Channel manager — tracks which WebSockets belong to which channel
class ChannelManager {
  private channels = new Map<string, Set<WebSocket>>();

  join(channel: string, ws: WebSocket) {
    if (!this.channels.has(channel)) this.channels.set(channel, new Set());
    this.channels.get(channel)!.add(ws);
  }

  leave(channel: string, ws: WebSocket) {
    this.channels.get(channel)?.delete(ws);
    if (this.channels.get(channel)?.size === 0) this.channels.delete(channel);
  }

  broadcast(channel: string, data: unknown, exclude?: WebSocket) {
    const msg = JSON.stringify(data);
    this.channels.get(channel)?.forEach((ws) => {
      if (ws !== exclude && ws.readyState === WebSocket.OPEN) {
        ws.send(msg);
      }
    });
  }
}
```

## Common Failure Modes

| Pattern | Why it fails / consequence |
|---|---|
| Auth only on connect, not per message | User loses permission mid-session; still receives events |
| No heartbeat / ping-pong | Dead connections leak memory; server thinks clients are alive |
| No reconnection logic | Tab sleep, network switch → permanent disconnect |
| Broadcasting everything to every client | Privacy leak (user sees other users' data); bandwidth waste |
| `EventEmitter` on multi-pod deployment | Events only reach clients on the same pod |
| WebSocket over HTTP (not HTTPS/WSS) | Blocked by proxies; no encryption |
| No backpressure on fast producer | Client can't consume fast enough → memory grows → OOM |
| Socket.IO used when plain WebSocket suffices | Extra protocol overhead, larger bundle, version compatibility |
| SSE without heartbeat comments | Proxies/load balancers close "idle" connections after 60s |

## Real-Time Review Checklist

- [ ] Technology choice matches use case (WebSocket for bidirectional, SSE for push)
- [ ] Auth verified on connect AND per-message/event
- [ ] Client reconnects with exponential backoff
- [ ] Server heartbeat detects and cleans dead connections
- [ ] Events filtered server-side per user/channel
- [ ] Multi-server: pub/sub layer (Redis, NATS) for cross-pod delivery
- [ ] Connection uses WSS/HTTPS, not plain WS/HTTP
- [ ] Rate limiting on incoming WebSocket messages
- [ ] Graceful shutdown drains connections before exit
- [ ] SSE endpoints send heartbeat comments to keep proxies alive

## Integration

- `domains/webdev/skill-api-graphql` — GraphQL subscriptions use WebSocket under the hood
- `domains/webdev/skill-api-rest` — REST endpoints that trigger real-time events (e.g., POST creates order → push notification)
- `domains/webdev/skill-auth` — token-based auth for WebSocket/SSE connections
- `domains/webdev/skill-backend` — real-time handlers sit alongside REST routes in the backend structure
- `domains/webdev/skill-devops` — WebSocket-aware load balancers, sticky sessions, Redis for pub/sub
- `domains/webdev/skill-observability` — connection count metrics, message rate, error rate
- `domains/webdev/skill-error-handling` — structured error messages over WebSocket

## Resources

- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [MDN EventSource (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)
- [ws (Node.js WebSocket library)](https://github.com/websockets/ws)
- [Socket.IO docs](https://socket.io/docs/) — when you need rooms, namespaces, and fallbacks built-in
- [NATS.io](https://nats.io/) — lightweight messaging for microservices
