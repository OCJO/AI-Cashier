import React, {useState} from 'react';
import { useHistory } from 'react-router-dom';

function Payment(){
    let history = useHistory();
    return(
        <div>
            {/* header */}
            {/* 결제 단계 배너 */}
            <div className="header">
                <div className="container">
                    <div className="header_banner">
                        <span className="header_name">OCJO 졸업 프로젝트</span>
                        <div className="pay_cource">
                            <div className="left_var">1.시작</div>
                            <div className="center_var">2.인식</div>
                            <div className="right_var_green">3.결제</div>
                        </div>
                    </div>
                </div>
            </div>
            {/*--결제 단계 배너 */}
            {/*-- header */}

            <div className="button-container">
                <div><button className="left-button">신용카드</button></div>
                <div><button className="right-button">현금</button></div>
            </div>

            <div className="button-container">
                <div><button className="left-button">모바일페이</button></div>
                <div><button className="right-button">포인트사용</button></div>
            </div>

            <button className="start-button" onClick={()=>{
                 history.push('/')
            }}>결제취소</button>
        </div>
        
    )
};

export default Payment