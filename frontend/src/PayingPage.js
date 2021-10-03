import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { Table } from 'react-bootstrap';
import { connect } from 'react-redux';
import './App.css';
import './Main.css';
import Modal from "./Modal.js";
import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

function Paying(props) {
    let history = useHistory();
    let total_price = 0;
    let img_src = "/" + props.imgstate
    const [categoryInfo, setCategoryInfo] = useState('');
    const [modalOpen, setModalOpen] = useState(false); // 모달창 플래그
    const openModal = () => {
        setModalOpen(true);
    }
    const closeModal = () => {
        setModalOpen(false);
    }

    return (
        <div>
            {/* header */}
            {/* 결제 단계 배너 */}
            <div className="header">
                <div className="container">
                    <div className="header_banner">
                        <span className="header_name">OCJO 졸업 프로젝트</span>
                        <div className="pay_cource">
                            <div className="left_var">1.시작</div>
                            <div className="center_var_green">2.인식</div>
                            <div className="right_var">3.결제</div>
                        </div>
                    </div>
                </div>
            </div>
            {/*--결제 단계 배너 */}
            {/*-- header */}

            {/* contents */}
            <div className="contents">
                <div className="container">
                    <div className="cont-cont">
                        <div className="column left_cont">
                            <img className="paying_img" src={img_src} />
                            <div className="button_container">
                                <button className="button" onClick={() => {
                                    console.log(props.state)
                                    openModal()
                                    axios({
                                        method: "get",
                                        url: 'http://localhost:8000/api/add_item/',
                                    }).then((Response) => {
                                        let itemCategoryInfo = JSON.parse(Response.data)
                                        setCategoryInfo(itemCategoryInfo['result'])
                                    })
                                        .catch((err) => {
                                            console.log(err)
                                        })
                                    // setCategoryInfo(b)
                                }}>항목추가</button>
                                <button className="button" onClick={() => {
                                    history.push('/payment')
                                }}>결제하기</button>
                                {/* 항목추가하기, 결제하기 버튼 */}
                            </div>      
                        </div>

                        <div className="column right_cont">
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
                                        props.state.map((a, i) => {
                                            // 구매총합계산
                                            let a_price = 0;
                                            a_price = a.price * a.value;
                                            total_price += a_price;
                                            return (
                                                <tr key={i}>
                                                    <td> {i + 1} </td>
                                                    <td> {a.name} </td>
                                                    <td> {a.price * a.value}</td>
                                                    <td>
                                                        {/* 수량감소버튼 */}
                                                        <button onClick={() => {
                                                            props.dispatch({ type: '-', payload: i })
                                                        }}>-</button>

                                                        {a.value}

                                                        {/* 수량증가버튼 */}
                                                        <button onClick={() => {
                                                            props.dispatch({ type: '+', payload: i })
                                                        }}>+</button>

                                                        {/* 품목제거버튼 */}
                                                        <button onClick={() => {
                                                            // a.deleteRow(i)
                                                            props.dispatch({ type: 'x', payload: i })
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
                </div>
            </div>
            {/* 결제테이블과 이미지 업로드  */}
            {/*-- contents */}

            {/* footer */}
            <div className="footer">
                <div className="container">footer</div>
            </div>
            {/*-- footer */}

            

            <div>
                <Modal open={modalOpen} close={closeModal} table={props.state} categoryInfo={categoryInfo} />
            </div>
        </div>

    )
};

function itemInfoState(state) {
    return {
        state: state.reducer,
        imgstate: state.reducer2,
        // price_state : state.price_reducer
    }
}

export default connect(itemInfoState)(Paying)
// export default Paying


// 보완할 점
// 1. 사진에 border값 주기 (o)
// 2. 버튼 사진밑으로 내리기 (o)
// 3. 중앙에 경계선 ()
// 4. 표 디자인 ()
// 5. 항목추가했을때 디자인 개선 ()

