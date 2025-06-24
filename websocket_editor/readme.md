# 웹 소켓으로 간단한 웹 에디터 구현
- node.js + websocket으로 server.js 구현
- 한 클라이언트가 Monaco editor를 통해 text를 입력하면 해당 서버에 접속 중인 다른 클라이언트의 editor 화면에도 같은 text가 보여짐

## 트러블 슈팅
### 문제1
monaco editor에 키보드 입력할 때마다 브라우저 콘솔에 
```
VM51:1 Uncaught SyntaxError: Unexpected token 'o', "[object Blob]" is not valid JSON
    at JSON.parse (<anonymous>)
    at socket.onmessage (index.html:34:26)
socket.onmessage	@	index.html:34
```
이라는 에러가 발생
### 해결
서버에서 클라이언트로 보내는 객체가 JSON 문자열이 아니라 blob 혹은 buffer 형태라서 클라이언트에서 JSON.parse(event.data)를 처리할 수 없음

서버에서 항상 문자열로 변환해서 응답을 보내주거나
클라이언트에서 blob을 받으면 조건문 처리해주기
```
ws.on('message', (msg) => {
  const msgStr = msg.toString(); //문자열로 변환
  wss.clients.forEach(client => {
    if (client !== ws && client.readyState === WebSocket.OPEN) {
      client.send(msgStr); // 항상 문자열로 전송
    }
  });
});
```
### 문제2



