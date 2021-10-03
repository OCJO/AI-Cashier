import logo from './logo.svg';
import React, { useState } from 'react';
import { Link, Route, Switch } from 'react-router-dom';
import { useHistory, useParams } from 'react-router-dom';
import axios from "axios";
import { connect } from 'react-redux';
import './Main.css';
import $ from "jquery";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";


function Main() {
    return (
        <div className="wrap">
            
            {/* header */}
            <div className="header">
                <div className="container">
                    <div className="header_banner">
                        <span className="header_name">OCJO 졸업 프로젝트</span>
                        <div className="pay_cource">
                            <div className="left_var green">1.시작</div>
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

                        <div className="column left_cont">
                            <h3>안녕하세요. <br/> <b>셀프 무인 계산대</b>입니다.</h3>
                            <div className="button_container">
                                <button className="button" onClick={() => {
                                    $('.img-upload').trigger('click')
                                }}>상품 업로드</button>
                                <form>
                                    <input className="img-upload" type="file" id="imgFile" />
                                    <input className="button" type="submit" value="인식 시작" />
                                </form>
                            </div>
                        </div>

                        <div className="column right_cont">
                            <div className="img_border">
                                <img className='' src="/img/main.jpg" alt="main image error"></img>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
            {/*-- contents */}

            {/* footer */}
            <div className="footer">
                <div className="container">footer</div>
            </div>
            {/*-- footer */}

        </div>
    )
}

export default Main;