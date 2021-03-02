<template>
  <v-row>
    <v-col cols="12">
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
    <p>
      <a :href="api_url">{{ api_url }}</a>にアクセスしてデータを取得します。
    </p>
    </v-col>
    <v-col cols="12">
      <v-btn
      dark
      @click="getUsers"
      >
      FLASK API TEST
      </v-btn>
    </v-col>
    <hr>
    <v-data-table
    dark
    dense
    :headers="headers"
    :items="user_datas"
    v-if="user_datas.length > 0"
    item-key="id"
    ></v-data-table>
  </v-row>
</template>

<script>
const axios = require('axios');
export default {
  data: function(){
    return {
      title:'axios WEB API',
      message:'Flaskで自作したWebAPIからデータを取得して表示するサンプル',
      user_datas:[],
      headers: [
        { text: 'ID', align: 'start', value: 'id' },
        { text: 'NAME', value: 'name' },
        { text: 'BIRTHDAY', value: 'birthday' },
      ],
      api_url: 'http://localhost:8000/api/v1/users'//http://localhost:5000/api/v1/users
    };
  },
  methods: {
    getUsers:function(event) {
      axios.get(this.api_url, {withCredentials: true})
      .then((res) => {
        console.log('通信成功');
        this.user_datas = res.data;
      })
      .catch((error) => {
        console.log('APIエラー');
        console.log(error);
      });
    },
  }
}
</script>