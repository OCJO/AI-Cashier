import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {BrowserRouter } from 'react-router-dom';
import {Provider} from 'react-redux';
import { combineReducers, createStore } from 'redux';

let detectionImg = 'Boundary box가 그려진 이미지 첨부'

function reducer2(state = detectionImg, action){
  return state
}


let itemInfo = [
    {id : 0, name : '콜라', price : 1200, quan : 2}, 
    {id : 1, name : '포스틱', price : 1500, quan : 1},
    {id : 2, name : '사이다', price : 1100, quan : 2},
    {id : 3, name : '비빔면', price : 1200, quan : 3},
    {id : 4, name : '허니버터칩', price : 1200, quan : 1},
    {id : 5, name : '메로나', price : 800, quan : 1},
];

function reducer(state = itemInfo, action){
  if (action.type === '+'){ //수량증가버튼
    let copy = [...state];
    copy[action.payload].quan++;
    return copy
  }else if (action.type === '-'){ //수량감소버튼
    let copy = [...state];
    copy[action.payload].quan--;
    if (copy[action.payload].quan <= 1){ //1 이하로 x
      copy[action.payload].quan = 1
      return copy
    }
  }else if (action.type === 'x'){ //삭제기능버튼
    let copy = [...state];
    copy.splice(action.payload,1);
    return copy
  }  
  return state
}


let store = createStore(combineReducers( {reducer, reducer2}) );

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <Provider store={store}>
        <App />
      </Provider>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
