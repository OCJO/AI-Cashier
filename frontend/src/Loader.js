import React from 'react';
import ReactLoading from 'react-loading';
import ScaleLoader from "react-spinners/ScaleLoader";
import './Main.css';

function Loader() {
    return (
        <div class="openModal modal">
            <div style={{
                position: "fixed",
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)",
            }}>
                {/* <h2>인식중입니다.</h2> */}
                <ScaleLoader height="80" width="32" color="#FF5C58" radius="8" />;
            </div> </div>);
}


export default Loader;

