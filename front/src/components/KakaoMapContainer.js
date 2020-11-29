import React, { useEffect, useState } from 'react';

const { kakao } = window;

const MapContainer = (props) => {

    useEffect(() => {
        // initialize kakao map.
        const container = document.getElementById('myMap');
		const options = {
			center: new kakao.maps.LatLng(33.450701, 126.570667),
			level: 3
		};
        const map = new kakao.maps.Map(container, options);

        // 일반 지도와 스카이뷰로 지도 타입을 전환할 수 있는 지도타입 컨트롤을 생성합니다
        var mapTypeControl = new kakao.maps.MapTypeControl();

        // 지도에 컨트롤을 추가해야 지도위에 표시됩니다
        // kakao.maps.ControlPosition은 컨트롤이 표시될 위치를 정의하는데 TOPRIGHT는 오른쪽 위를 의미합니다
        map.addControl(mapTypeControl, kakao.maps.ControlPosition.TOPRIGHT);

        // 지도 확대 축소를 제어할 수 있는  줌 컨트롤을 생성합니다
        var zoomControl = new kakao.maps.ZoomControl();
        map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT);
        
        // get current location.
        if(navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((position) => {
                map.setCenter(new kakao.maps.LatLng(position.coords.latitude, position.coords.longitude));
                console.log('current position : latitude: ' + position.coords.latitude + ' longitude:  ' + position.coords.longitude);
            })
        }

        // marker positon
        var markerPosition  = new kakao.maps.LatLng(37.5586, 126.9342); 

        // render marker
        var marker = new kakao.maps.Marker({
            position: markerPosition
        });

        // 마커가 지도 위에 표시되도록 설정합니다
        marker.setMap(map);

    }, []);

    return (
        <div id='myMap' style={{
            width: '500px', 
            height: '500px'
        }}></div>
    );
}

export default MapContainer;