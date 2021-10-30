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
                        <form>
                            <label for="largeCategoryLabel">대분류를 선택해주세요 : </label>
                            <select className="largeCategory" name="large_Category" onChange={(e) => {
                                setLcategory(e.target.value)
                                setSarray(categoryInfo[e.target.value])
                            }}>
                                <option value="none" selected disabled>선택해주세요</option>
                                {
                                    Object.entries(categoryInfo).map((a, i) => {
                                        return (
                                            <option key={i} value={a[0]}>{a[0]}</option>
                                        )
                                    })
                                }
                            </select>

                            {/* 소분류는 대분류 선택시에 백앤드에 요청을 보내 원하는 값을 가져와야 함(보류) */}

                            <br></br>

                            <label for="smallCategoryLabel">소분류를 선택해주세요 : </label>
                            <select className="smallCategory" name="smallCategory" onChange={(e) => {
                                console.log("내가 선택한 소분류 : " + e.target.value)
                                setScategory(e.target.value)
                                setSid(categoryInfo[lCategory][e.target.value])
                            }}>
                                <option value="none" selected disabled>선택해주세요</option>
                                {
                                    Object.keys(sArray).map((item, index) => {
                                        return (
                                            <option key={index} value={item}>{item}</option>
                                        )
                                    })
                                }
                            </select>
                        </form>
                        {/*form*/}
                    </div>
                    {/* 대분류, 소분류 선택 폼 */}

                    <div className="modal-footer">
                        <button className="close" onClick={() => {
                            console.log(props)
                            // 원하는 값을 가져와야 함(Large, Small category에 맞는 Id로 요청, 해당 Price를 받음 수량은 '1'로 고정)
                            axios({
                                method: "post",
                                url: 'http://localhost:8000/api/add_item/',
                                data: { pid: sId }
                            }).then((Response) => {
                                console.log("내가 받은 가격 : " + Response.data)
                                let itemPrice = JSON.parse(Response.data)

                                if (sId) { // 대분류, 소분류를 선택한 경우에만 동작하도록
                                    props.dispatch({ type: '테이블추가', payload: { pid: sId, name: sCategory, price: itemPrice['price'], value: 1 } })
                                }
                                console.log(table)
                                // await pushItem()
                            })
                                .catch((err) => {
                                    console.log(err)
                                })
                            //초기화
                            setSid('')
                            setScategory('')
                            setLcategory('')
                            setSarray('')

                            close()

                        }} > 추가  </button>
                        <button className="close" onClick={() => {
                            //초기화
                            setSid('')
                            setScategory('')
                            setLcategory('')
                            setSarray('')

                            close()
                        }}> 취소 </button>

                        {/* <div className="modal-footer"></div> */}

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