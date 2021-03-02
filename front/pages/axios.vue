<template>
  <v-row>
    <v-col cols="12">
    <h1>{{ title }}</h1>
    <p style="color: red;">{{ message }}</p>
    <p>{{ api_url }}からデータを取得します。</p>
    </v-col>
    <v-col cols="12">
      <v-form 
      ref="form">
        <v-col cols="6">
          <v-text-field 
          v-model="id"
          label="ID" 
          :rules="[validations.required, validations.id_input_check]"
          />
        </v-col>
        <v-col cols="6">
          <v-btn 
          @click="doClick"
          dark
          >
          ADD Data
          </v-btn>
        </v-col>
      </v-form>
    </v-col>
    <hr>
    <v-data-table
    dense
    :headers="headers"
    :items="json_data"
    v-if="json_data.length > 0"
    item-key="id"
    ></v-data-table>
  </v-row>
</template>

<script>
const axios = require('axios');

export default {
  data: function(){
    return {
      title:'Axios',
      message:'axios sample.',
      id:'',
      json_data:[],
      headers: [
        { text: 'ユーザーID', align: 'start', value: 'userId' },
        { text: 'ID', value: 'id' },
        { text: 'タイトル', value: 'title' },
        { text: '内容', value: 'body' },
      ],
      validations: {
        required: v => !!v || this.messages.required_error,
        id_input_check: v => new RegExp('^([1-9]{0,1}[0-9]{0,1}|100)$').test(v) || this.messages.input_range_error,
      },
      messages: {
        required_error: '必須項目です',
        input_range_error: '1～100の範囲内で入力してください',
      },
      api_url: 'https://jsonplaceholder.typicode.com/posts/',
    };
  },
  methods: {
    doClick:function(event) {
      //formの入力エラーがない場合
      if(this.$refs.form.validate()){
        axios.get(this.api_url + this.id)
        .then((res) => {
          this.message = 'get ID=' + this.id;
          //if(this.json_data.map(data => data.id).some( id => id === res.data.id)){
          if(this.json_data.some( data => data.id === res.data.id)){
            this.message = '既に追加済みのidです';
          }else{
            this.json_data.push(res.data);
          }
          
        })
        .catch((error) => {
          this.message = 'データが見つかりませんでした。';
          console.log(error);
        });
      }else{
        console.log('form invalid');
      }
    },
  },
}
</script>


<style>
input {
  font-size:14pt;
}
button {
  font-size:14pt;
}
</style>