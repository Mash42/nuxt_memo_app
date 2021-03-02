<template>
  <v-row>
    <v-col cols="6">
      <h1 class="mt-2">{{ page_title }}</h1>
        <v-form
          ref="form"
          v-model="form_valid"
          class="mt-2"
        >
          <v-text-field
            outlined
            v-model="title"
            label="タイトル"
            autocomplete="off"
            :rules="[rules.required, rules.max_length_title]"
          />
          <v-textarea
            v-model="content"
            label="内容"
            auto-grow
            outlined
            :rules="[rules.required, rules.max_length_content]"
          ></v-textarea>
          <v-btn v-if="!modify_flg" @click="insert" color="green" elevation="5" :disabled="!form_valid">
            <v-icon>mdi-content-save</v-icon>保存
          </v-btn>
          <v-btn v-if="!modify_flg" @click="form_reset" color="blue" elevation="5">
            <v-icon>mdi-autorenew</v-icon>クリア
          </v-btn>
          <v-btn v-if="modify_flg" @click="modify_execute" color="pink darken-2" elevation="5" :disabled="!form_valid" class="mr-4">
            <v-icon>mdi-content-save-all</v-icon>修正
          </v-btn>
          <v-btn v-if="modify_flg" @click="modify_cancel" color="light-blue lighten-4" elevation="5">
            <v-icon>mdi-cancel</v-icon>キャンセル
          </v-btn>
        </v-form>
    </v-col>
    <v-col cols="6">
      <v-btn 
        v-if="memo_list.length > 0" 
        @click="table_color_chg"
        :color="color_chg_btn.color"
        :class="color_chg_btn.class"
      >
        {{ color_chg_btn.text }}
      </v-btn>
      <v-data-table 
        :headers="memo_list_headers"
        :items="memo_list"
        v-if="memo_list.length > 0"
        item-key="ID"
        :dark="dark_table"
      >
        <template v-slot:item.id="{ item }">
          <div @click="click_table_row(item)">
            {{ item.id }}
          </div>
        </template>
        <template v-slot:item.title="{ item }">
          <div @click="click_table_row(item)">
            {{ item.title }}
          </div>
        </template>
        <template v-slot:item.create_day="{ item }">
          <div @click="click_table_row(item)">
            {{ item.create_day }}
          </div>
        </template>
        <template v-slot:item.create_time="{ item }">
          <div @click="click_table_row(item)">
            {{ item.create_time }}
          </div>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-icon
            small
            @click="copy(item)"
            :color="dark_table?'white':'black'"
          >
            mdi-content-copy
          </v-icon>
          <v-icon
            small
            @click="modify(item)"
            :color="dark_table?'white':'black'"
          >
            mdi-pencil
          </v-icon>
          <v-icon
            small
            @click="remove(item)"
            :color="dark_table?'white':'black'"
          >
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data: function(){
    return {
      dark_table: false,
      page_title: 'メモアプリ',
      title:'',
      content:'',
      modify_memo: null,
      modify_flg: false,
      memo_list: [],
      memo_list_headers: [
      { text: 'メモID', align: 'start', value: 'id'},
      { text: 'タイトル', value: 'title' },
      { text: '作成日', value: 'create_day' },
      { text: '作成時間', value: 'create_time' },
      { text: 'Actions', value: 'actions', sortable: false },
      ],
      color_chg_btn: {
        color: 'black',
        class: {
          active: true,
          'white--text': true,
        },
        text: 'ダークモードへ'
      },
      form_valid: true,
      rules: {
          required: value => !!value || '必須です。',
          max_length_title: value => value.length <= 15 || 'この項目は最大15文字です。',
          max_length_content: value => value.length <= 400 || 'この項目は最大400文字です。',
      },
    };
  },
  methods: {
    insert: async function(){
      const response_insert = await this.api_memo_insert(this.title, this.content);
      console.log(response_insert);
      const response_get_memo = await this.api_get_memos();
      console.log(response_get_memo);
      this.memo_list = response_get_memo.data;
      this.form_reset();
    },
    modify: function(item){
      this.modify_flg = true;
      this.title = item.title;
      this.content = item.content;
      this.modify_memo = item;
    },
    modify_execute: async function(){
      const response = await this.api_memo_modify(this.modify_memo.id, this.title, this.content);
      console.log(response);
      const response_get_memo = await this.api_get_memos();
      console.log(response_get_memo);
      this.memo_list = response_get_memo.data;
      this.form_reset();
    },
    modify_cancel: function(){
      this.form_reset();
    },
    copy: function(item){
      this.modify_flg = false;
      this.title = item.title;
      this.content = item.content;
    },
    form_reset: function(){
      this.title = '';
      this.content = '';
      this.modify_flg = false;
      this.$refs.form.resetValidation();
    },
    remove: async function(item){
      if(this.modify_flg && this.modify_memo.id === item.id){
        alert("現在編集中のメモは削除できません。");
        return;
      }
      const response_delete = await this.api_memo_delete(item.id);
      console.log(response_delete);
      const response_get_memo = await this.api_get_memos();
      console.log(response_get_memo);
      this.memo_list = response_get_memo.data;
    },
    click_table_row: function(item) {
      this.copy(item);
    },
    table_color_chg: function() {
      this.dark_table = !this.dark_table;
      this.color_chg_btn.color = this.dark_table?'white':'black'
      this.color_chg_btn.class = this.dark_table?'':'white--text'
      this.color_chg_btn.text = this.dark_table?'ホワイトモードへ':'ダークモードへ'
    },
    api_get_memos: async function(){
      try{
        return (await this.$axios.get('http://localhost:8000/api/v1/memo'))
      } catch (error) {
        return error.response.status;
      }
    },
    api_memo_insert: async function(title, content){
      try{
        return (
          await this.$axios
          .post('http://localhost:8000/api/v1/memo/insert',
            {"title": title,
             "content": content,
            }
          )
        );
      } catch (error) {
        throw errro.response.status
      }
    },
    api_memo_modify: async function(id, title, content){
      try{
        return (
          await this.$axios
          .post('http://localhost:8000/api/v1/memo/modify',
            {"id": id,
             "title": title,
             "content": content,
            }
          )
        );
      } catch (error) {
        throw errro.response.status
      }
    },
    api_memo_delete: async function(id){
      try{
        return (
          await this.$axios
          .post('http://localhost:8000/api/v1/memo/delete',
            {"id": id}
          )
        );
      } catch (error) {
        throw errro.response.status;
      }
    },
  },
  created: async function(){
    console.log('created');
    const response = await this.api_get_memos();
    this.memo_list = response.data;
  },
}
</script>