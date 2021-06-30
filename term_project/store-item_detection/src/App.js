import logo from './logo.svg';
import './App.css';
import React, {useState} from 'react';
import $ from "jquery";
import Payment from "./PaymentSelectPage.js";
import Paying from "./PayingPage.js";
import { Link, Route, Switch} from 'react-router-dom';
import { useHistory, useParams } from 'react-router-dom';

function App() {
  let history = useHistory();
  const [imgBase64, setImgBase64] = useState(""); // 파일 base64
  const [imgFile, setImgFile] = useState(null);	//파일

  const handleChangeFile = (event) => {
    let reader = new FileReader();

    reader.onloadend = () => {
      // 2. 읽기가 완료되면 아래코드가 실행됩니다.
      const base64 = reader.result;
      if (base64) {
        setImgBase64(base64.toString()); // 파일 base64 상태 업데이트
      }
      
    }
    if (event.target.files[0]) {
      reader.readAsDataURL(event.target.files[0]); // 1. 파일을 읽어 버퍼에 저장합니다.
      setImgFile(event.target.files[0]); // 파일 상태 업데이트
    }
  }

  return (
    <div className="App">

      <Switch>
        {/* 메인페이지 라우팅 */}
        <Route exact path="/">
          <div className="container">
            <div className = "greenvar">1.상품업로드</div>
            <div className = "var">2.상품 항목 확인</div>
            <div className = "var">3.결제 수단</div>
          </div>
          
          <div className= "my-alert">구매할 상품의 이미지를 등록하세요.</div>

          <div className= "img-border">
            <img className='' src={imgBase64}></img>
          </div>

          <button className="start-button" onClick={()=>{
            $('.img-upload').trigger('click')
          }}>이미지 업로드</button>
          <button className="start-button" onClick={()=>{
            history.push('/paying')
          }}>인식 시작</button>
          <input className="img-upload" type="file" name="imgFile" id="imgFile" onChange={handleChangeFile}/>
        </Route>
      

        {/* 결제상품리스트 확인 페이지 라우팅 */}
        <Route path="/paying">
          <Paying></Paying>
        </Route>


        {/* 결제수단 선택 페이지 라우팅 */}
        <Route path="/payment">
          <Payment></Payment>
        </Route>
      </Switch>
      
    </div>
  );
}

export default App;
