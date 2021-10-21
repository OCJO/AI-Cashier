import logo from './logo.svg';
// import './App.css';
import React, { useState } from 'react';
import $ from "jquery";
import Payment from "./PaymentSelectPage.js";
import Paying from "./PayingPage.js";
import Main from "./new_mainpage.js";
import './Main.css';
import { Link, Route, Switch } from 'react-router-dom';
import { useHistory, useParams } from 'react-router-dom';
import axios from "axios";
import { connect } from 'react-redux';
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";


function App(props) {
  let history = useHistory();
  const [imgBase64, setImgBase64] = useState("/static/default_img.jpg"); // 파일 base64
  const [imgFile, setImgFile] = useState(null);	//파일

  const handleChangeFile = (event) => {
    let reader = new FileReader();

    reader.onloadend = () => {
      // 2. 읽기가 완료되면 아래코드가 실행
      const base64 = reader.result;
      if (base64) {
        setImgBase64(base64.toString()); // 파일 base64 상태 업데이트
      }

    }
    if (event.target.files[0]) {
      reader.readAsDataURL(event.target.files[0]); // 1. 파일을 읽어 버퍼에 저장
      setImgFile(event.target.files[0]); // 파일 상태 업데이트
    }
  }

  const [textList, textListchange] = useState();	//파일

  // 이미지를 백엔드에 전송하는 함수 
  const getDetectResult = async (e) => {
    e.preventDefault()
    var fileInput = document.querySelector(".img-upload")

    let formData = new FormData();
    formData.append("image", imgFile);

    axios({
      method: "post",
      url: 'http://localhost:8000/api/object_detect/',
      headers: { "content-type": "multipart/form-data", },
      data: formData
    }).then((Response) => {
      var table_info = JSON.parse(Response.data)
      props.dispatch({ type: '인식시작', payload: table_info })
      history.push('/paying') // 결제리스트 페이지로 이동
    })
      .catch((err) => {
        console.log(err)
      })
  }

  return (
    <div className="App">

      <Switch>

        {/* 메인페이지 라우팅 */}
        <Route exact path="/">
          {/* header */}
          <div className="header">
            <div className="container">
              <div className="header_banner">
                <span className="header_name">OCJO 졸업 프로젝트</span>
                <div className="pay_cource">
                  <div className="left_var_green">1.시작</div>
                  <div className="center_var">2.인식</div>
                  <div className="right_var">3.결제</div>
                </div>
              </div>
            </div>
          </div>
          {/*-- header */}

          {/* contents */}
          <div className="contents">
            <div className="container">
              <div className="cont-cont">

                {/* 상품업로드, 인식시작버튼 */}
                <div className="column left_cont">
                  <h3>안녕하세요. <br /> <b>셀프 무인 계산대</b>입니다.</h3>
                  <div className="button_container">
                    <button className="button" onClick={() => {
                      $('.img-upload').trigger('click')
                    }}>상품 업로드</button>

                    <form onSubmit={getDetectResult}> 
                      <input className="img-upload" type="file" id="imgFile" onChange={handleChangeFile}/>
                      <input className="button" type="submit" value="인식 시작" />
                    </form>
                  </div>
                </div>
                {/*-- 상품업로드, 인식시작버튼 */}

                {/* 이미지 입력란 */}
                <div className="column right_cont">
                  <div className="img_border">
                    <img className='reco_img' src={imgBase64} alt="main image error"></img>
                  </div>
                </div>
                {/*--이미지 입력란 */}    

              </div>
            </div>
          </div>
          {/*-- contents */}

          {/* footer */}
          <div className="footer">
            <div className="container">
              <span className="header_name">OCJO 졸업 프로젝트</span>
            </div>
          </div>
          {/*-- footer */}

         
        </Route>
        {/* //메인페이지 라우팅 */}


        {/* 결제상품리스트 확인 페이지 라우팅 */}
        <Route path="/paying">
          <Paying></Paying>
        </Route>
        {/* //결제상품리스트 확인 페이지 라우팅 */}


        {/* 결제수단 선택 페이지 라우팅 */}
        <Route path="/payment">
          <Payment></Payment>
        </Route>
        {/* //결제수단 선택 페이지 라우팅 */}

        새로운 메인페이지 제작중입니다.
        <Route path="/main">
          <Main></Main>
        </Route>
      </Switch>

    </div>
  );
}

// export default App;
function itemInfoState(state) {
  return {
    state: state.reducer,
    imgstate: state.reducer2,
  }
}

export default connect(itemInfoState)(App)

// 보완사항
// - 상품업로드나 인식시작 버튼에 hover효과 주기 (o)
// - 이미지 들어가는 border부분에 원래 default 이미지 넣어주기
// 원래 이미지가 존재하다가 상품업로드버튼을 누르고 이미지를 넣어줄때 기본 이미지가 사라지고 선택된 사진이 들어가도록
// 업로드 취소, 인식시작 버튼을 왼쪽, 이미지박스안에 '결제할 상품 이미지 업로드하기'문구와 버튼