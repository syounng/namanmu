# 웹 소켓으로 간단한 웹 에디터 구현
- node.js + websocket으로 server.js 구현
- 한 클라이언트가 Monaco editor를 통해 text를 입력하면 해당 서버에 접속 중인 다른 클라이언트의 editor 화면에도 같은 text가 보여짐

# 트러블 슈팅
## 문제
monaco editor에 키보드 입력할 때마다 브라우저 콘솔에 
```
VM51:1 Uncaught SyntaxError: Unexpected token 'o', "[object Blob]" is not valid JSON
    at JSON.parse (<anonymous>)
    at socket.onmessage (index.html:34:26)
socket.onmessage	@	index.html:34
```
이라는 에러가 발생
## 해결
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
## 문제
![image](https://github.com/user-attachments/assets/73c4c85b-98bb-4a08-abca-104e1184643a)
느리게 한 글자씩 입력하는 경우 정상 동작
그러나 빠른 속도로 입력하는 경우 먹통이 됨
브라우저 콘솔에 아무것도 출력되지 않아서 디버깅 필요해보임

## 해결
```
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
        console.log(`client: ${client.id} message: ${msgStr}`);
      }else{
        console.log(`client: ${client.id} `);
      }
    });
  });
```
이런 식으로 콘솔 로그를 찍어봤는데
![image](https://github.com/user-attachments/assets/1a1e6adb-4a2f-4346-b2da-1b0ff810c06a)
client 1, 2, 3 동시 접속했을 때 client 1이 한 글자만 수정해도 연쇄적으로 이벤트가 발생할 수 있음
![스크린샷 2025-06-24 오후 9 24 43](https://github.com/user-attachments/assets/3d28f8cd-c1ba-4978-807b-9775ccb3da24)

클라이언트 1이 텍스트 수정 
-> 본인을 제외한 나머지 클라이언트와 비교해서 텍스트가 다르면 본인 텍스트로 덮어쓰기 (broadcast)

여기서 문제점이 특정 클라이언트가 실시간으로 텍스트를 수정하면 무조건 나머지 클라이언트들과 텍스트가 달라지므로 항상 서버에 (클라이언트 수-1)^2번 만큼의 요청이 발생한다는 점이다.

그래서 여러 클라이언트가 동시 접속한 상황에서 굉장히 빠른 속도로 텍스트를 수정하게 되면 서버에 요청이 꼬이면서 에러가 발생하게 된다.
![스크린샷 2025-06-24 오후 9 31 51](https://github.com/user-attachments/assets/a64f6ad0-4b2c-4a3a-a1ad-66e287934514)
키보드를 좀만 빨리 치면 이렇게 똑같은 요청이 무한루프된다.

해결 방법은 

## 문제
<img width="757" alt="스크린샷 2025-06-24 오후 5 22 09" src="https://github.com/user-attachments/assets/234bcbf8-f016-48b4-82cc-0d8294f31ad6" />
약 10개의 클라이언트가 동시에 접속할 경우 연결 속도가 매우 느려짐 (8번째 연결부터 약 5초 이상 소요)

## 문제
서버에 새로운 클라이언트가 접속하면 기존 클라이언트들이 써둔 코드가 보이지 않고 빈 페이지가 뜸
새로운 클라이언트가 빈 페이지에 쓰기를 시작하면 기존 클라이언트들이 써둔 코드가 사라지고 새로운 클라이언트가 쓰는 내용으로 덮어씌워짐
