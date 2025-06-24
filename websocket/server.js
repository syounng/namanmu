// ① 웹소켓 서버 라이브러리 설치 필요: npm install ws
const WebSocket = require('ws');

// ② 3000번 포트에 웹소켓 서버 열기
const wss = new WebSocket.Server({ port: 3000 });

wss.on('connection', function connection(ws) {
  console.log('클라이언트가 연결됨!');

  ws.on('message', function message(data) {
    console.log('받은 메시지:', data.toString());

    // 연결된 모든 클라이언트에게 메시지 보내기
    wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(data.toString());
      }
    });
  });
});
