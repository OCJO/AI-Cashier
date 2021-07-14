# AI-Cashier

# 인공지능을 활용한 편의점 계산 도우미
  
충남대학교 졸업프로젝트  _ (주)플랜아이 산업체 프로젝트
팀명: 오쪼  
팀원: 오재성(팀장), 조윤희, 조윤혁     
  
- Frontend : React  
- Backend : Django
- AI : Yolov5

DB
----- 
1. 상품 정보 테이블
    - pid / category_L / name / price
2. 재고 테이블
    - pid / value / modify_date


API
----- 
1. object_detect_api
    [post]
    - request : 이미지 파일
    - do : 이미지 파일 저장 / ai 모델 load  
    - reponse : 결과 이미지 path / 상품 정보들 / 상태코드  

2. add_item_api
    [get]  
    - reponse : 대분류(category_L) 마다의 name, id / 상태코드  
    [post]
    - request : id
    - do : id에 해당하는 가격 가져옴
    - reponse : 가격  

3. payment_api
    - request : ID, 수량 , 총 결제 금액 받음 
    - do : 재고 테이블 갱신
    - reponse : ID, 수량 , 총 결제 금액

  
+ backend 폴더 밑에 'rest_settings.py' 넣어야함! -> 로지한테 있음  

