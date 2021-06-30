import React, {useState} from 'react';
import { useHistory } from 'react-router-dom';

function Payment(){
    let history = useHistory();
    return(
        <div>
            <div className="container">
                <div className = "var">1.상품업로드</div>
                <div className = "var">2.상품 항목 확인</div>
                <div className = "greenvar">3.결제 수단</div>
            </div>

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