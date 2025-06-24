const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 3001 });

let clientIdCounter = 1;

wss.on('connection', (ws) => {
    //ws는 연결된 특정 클라이언트 객체
    ws.id = clientIdCounter++;
    console.log(`클라이언트가 연결됨! ID: ${ws.id}`);

    // 클라이언트가 socket.send()로 메시지를 보내면 실행되는 이벤트 핸들러
  ws.on('message', (msg) => {
    // 다른 클라이언트에게 브로드캐스트
    // 현재 연결된 모든 클라이언트 목록을 순회하면서 메시지 전송
    // 자기 자신은 제외하고 메시지 전송
    // wss.clients는 현재 연결된 모든 클라이언트들의 목록
    const msgStr = msg.toString();
    wss.clients.forEach(client => {
      if (client !== ws && client.readyState === WebSocket.OPEN) {
        client.send(msgStr);
      }
    });
  });
});
