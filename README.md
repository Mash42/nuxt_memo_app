# nuxt_memo_app

## 起動方法(API)

+ apiフォルダへ移動  
`cd api`

+ コンテナ起動  
`docker-compose up -d --build`

## 起動方法(Front)

+ frontフォルダへ移動  
`cd front`

+ 既存プロジェクトの読み込み  
`npm install`

+ axiosのインストール  
`npm install axios --save`

+ プロジェクトを開発モードで起動  
`npm run dev`

##　各URL

+ Front(WEB画面)  
http://localhost:3000  

+ API(データベース操作)  
http://localhost:8000/api/v1/memo  
http://localhost:8000/api/v1/memo/insert  
http://localhost:8000/api/v1/memo/modify  
http://localhost:8000/api/v1/memo/delete  

+ phpMyAdmin(データベースGUI)  
http://localhost:8080  


