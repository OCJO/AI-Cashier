import React, {useState} from 'react';
import { useHistory } from 'react-router-dom';
import { Table } from 'react-bootstrap';
import { connect } from 'react-redux';

function Paying(props){
    let history = useHistory();
    let total_price = 0;
    let img_src = "/" + props.imgstate
    return(
        <div>
            <div className="container">
                <div className = "var">1.상품업로드</div>
                <div className = "greenvar">2.상품 항목 확인</div>
                <div className = "var">3.결제 수단</div>
            </div>

            <div className="lr-container">
                <div className="left-img">
                    <img src = {img_src} /> 
                        
                </div>
                <div className="right-table">테이블
                    <Table className="table-type">
                        <thead>
                            <tr>
                                <th>NO.</th>
                                <th>상품명</th>
                                <th>가격</th>
                                <th>수량</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                props.state.map((a,i)=>{
                                    // 구매총합계산
                                    let a_price = 0;
                                    a_price = a.price * a.value;
                                    total_price += a_price;
                                    return (
                                        <tr key={i}>
                                            <td> { i+1 } </td>
                                            <td> { a.name } </td>
                                            <td> { a.price * a.value }</td>
                                            <td> 
                                                {/* 수량감소버튼 */}
                                                <button onClick={()=>{
                                                    props.dispatch( { type : '-', payload : i } )    
                                                }}>-</button> 

                                                { a.value } 
                                                
                                                {/* 수량증가버튼 */}
                                                <button onClick={()=>{
                                                    props.dispatch( { type : '+', payload : i } )
                                                }}>+</button>

                                                {/* 품목제거버튼 */}
                                                <button onClick={()=>{
                                                    // a.deleteRow(i)
                                                    props.dispatch( { type : 'x', payload : i } )
                                                }}>x</button>
                                            </td>
                                        </tr>
                                    )
                                })
                            }
                            <tr>
                                <td>총합</td>
                                <td colSpan="3">{total_price}원</td>
                            </tr>
                        </tbody>
                    </Table>
                </div>
            </div>

            <button className="start-button">항목추가</button>
            <button className="start-button" onClick={()=>{
                history.push('/payment')
            }}>결제하기</button>
        </div>

    )
};

function itemInfoState(state){
    return {
        state : state.reducer,
        imgstate : state.reducer2,
        // price_state : state.price_reducer
    }
}

export default connect(itemInfoState)(Paying)
// export default Paying