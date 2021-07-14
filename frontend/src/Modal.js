import React, { useState } from 'react';
import './App.css';
import { useForm } from "react-hook-form";

const Modal = ( props ) => {
    const { open, close, table, categoryInfo} = props // 열기, 닫기, 모달 헤더 텍스트를 부모로부터 받아옴
    let selectedItem = ''  // 대분류 select문에서 선택된 item
    

    const [sItem, setSitem]  = useState(''); //ref의 선택자인 register
    const [sArray, setSarray] = useState(''); // 대분류 선택에 따라 담길 소분류 리스트 
    // let arr = ['a', 'b'] // 대분류 선택에 따라 담길 소분류 리스트 
    // const selectvalue = (e) => {
    //     selectedItem = e.target.value
    //     console.log(e.target.value)
    //     setSitem(e.target.value)
    // }
    
    return (
        // 모달이 열릴때 openModal 클래스가 생성된다.
        
        <div className={ open ? 'openModal modal' : 'modal' }>
            { open ? ( 
                <div className="modal-total">
                    <div className="modal-form">
                        <form>
                            <label for="largeCategoryLabel">대분류를 선택해주세요 : </label>
                            <select className="largeCategory" name="large_Category"  onChange={(e)=>{
                                setSitem(e.target.value)
                                setSarray(categoryInfo[e.target.value])   
                            }}>

                                <option value="none" selected disabled>선택해주세요</option>
                                {
                                    Object.entries(categoryInfo).map( (a,i)=>{
                                        return (
                                            <option key={i} value={a[0]}>{a[0]}</option>
                                        )
                                    })
                                }
                            </select>

                            {/* 소분류는 대분류 선택시에 백앤드에 요청을 보내 원하는 값을 가져와야 함(보류) */}

                            <br></br>
                        
                            <label for="smallCategoryLabel">소분류를 선택해주세요 : </label>
                            <select className="smallCategory" name="smallCategory">
                                <option value="none" selected disabled>선택해주세요</option>
                                {
                                    Object.keys(sArray).map((item, index)=>{
                                        return(
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
                        <button className="close" onClick={()=>{
                            // 원하는 값을 가져와야 함(Large, Small category 전송 후 받은 Id, Price, 수량은 '1'로 고정)
                            table.push({id : 0, name : '콜라', price : 1200, value: 1})
                            //axios
                            setSarray('')
                            close()
                        }} > 추가  </button>
                        <button className="close" onClick={()=>{
                            setSarray('')
                            close()
                        }}> 취소 </button>

                        <div className="modal-footer"></div>
                        
                    </div>
                    {/* 추가, 취소버튼  */}
                </div>

            ) : null }
        </div>
    )
}


export default Modal