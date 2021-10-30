import React, { useState } from 'react';
import './App.css';
import { useForm } from "react-hook-form";
import axios from "axios";
import { connect } from 'react-redux';
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";


const Modal = (props) => {
    const { open, close, table, categoryInfo } = props // 열기, 닫기, 모달 헤더 텍스트를 부모로부터 받아옴
    const [sArray, setSarray] = useState('') // 대분류 선택에 따라 담길 소분류 리스트 
    const [lCategory, setLcategory] = useState('') // 선택한 대분류
    const [sCategory, setScategory] = useState('') // 선택한 소분류
    const [sId, setSid] = useState('') // 선택한 소분류의 Id 값

    return (
        // 모달이 열릴때 openModal 클래스가 생성된다.
        <div className={open ? 'openModal modal' : 'modal'}>
            {open ? (
                <div className="modal-total">
                    <div className="modal-form">
                        <div className="pay_border">
                            <h2 className="paytext1">결제</h2>
                            <div className="paytotal_border">
                                <div className="paytotal_border_text">결제금액</div>
                                <div className="paytotal_border_total">5000원</div>                  
                            </div>

                            {/* 현금, 카드 결제버튼 */}
                            <div className="paybutton">
                                <h3 className="paytext2">결제 수단을 선택해주세요</h3>
                                <div className="cash" onClick={() => {
                                    // console.log(props)
                                    // // 원하는 값을 가져와야 함(Large, Small category에 맞는 Id로 요청, 해당 Price를 받음 수량은 '1'로 고정)
                                    // axios({
                                    //     method: "post",
                                    //     url: 'http://localhost:8000/api/add_item/',
                                    //     data: { pid: sId }
                                    // }).then((Response) => {
                                    //     console.log("내가 받은 가격 : " + Response.data)
                                    //     let itemPrice = JSON.parse(Response.data)

                                    //     if (sId) { // 대분류, 소분류를 선택한 경우에만 동작하도록
                                    //         props.dispatch({ type: '테이블추가', payload: { pid: sId, name: sCategory, price: itemPrice['price'], value: 1 } })
                                    //     }
                                    //     console.log(table)
                                    //     // await pushItem()
                                    // })
                                    //     .catch((err) => {
                                    //         console.log(err)
                                    //     })

                                    close()

                                }}>
                                    현금
                                </div>
                            
                                <div className="card" onClick={() => {
                                    console.log(props)
                                    // 원하는 값을 가져와야 함(Large, Small category에 맞는 Id로 요청, 해당 Price를 받음 수량은 '1'로 고정)
                                    // axios({
                                    //     method: "post",
                                    //     url: 'http://localhost:8000/api/add_item/',
                                    //     data: { pid: sId }
                                    // }).then((Response) => {
                                    //     console.log("내가 받은 가격 : " + Response.data)
                                    //     let itemPrice = JSON.parse(Response.data)

                                    //     if (sId) { // 대분류, 소분류를 선택한 경우에만 동작하도록
                                    //         props.dispatch({ type: '테이블추가', payload: { pid: sId, name: sCategory, price: itemPrice['price'], value: 1 } })
                                    //     }
                                    //     console.log(table)
                                    //     // await pushItem()
                                    // })
                                    //     .catch((err) => {
                                    //         console.log(err)
                                    //     })
                                    // //초기화
                                    // setSid('')
                                    // setScategory('')
                                    // setLcategory('')
                                    // setSarray('')

                                    close()

                                }}>
                                    카드
                                </div>
                            </div>
                            {/* -- 현금, 카드 결제버튼 */}
                        </div>
                        
                    </div>
                    {/* 대분류, 소분류 선택 폼 */}

                    <div className="modal-footer">
                        <button className="close" onClick={() => {
                            //초기화
                            close()
                        }}> 취소 </button>

                    </div>
                    {/* 추가, 취소버튼  */}
                </div>

            ) : null}
        </div>
    )
}

// export default Modal
function itemInfoState(state) {
    return {
        state: state.reducer,
        imgstate: state.reducer2,
    }
}

export default connect(itemInfoState)(Modal)