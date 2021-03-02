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
            <v-icon>mdi-content-save</v-icon>クリア
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
        v-if="memo.length > 0" 
        @click="table_color_chg"
        :color="color_chg_btn.color"
        :class="color_chg_btn.class"
      >
        {{ color_chg_btn.text }}
      </v-btn>
      <v-data-table 
        :headers="memo_list_headers"
        :items="memo_list"
        v-if="memo.length > 0"
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
  computed: {
    memo: function(){ 
      return this.$store.state.memo.memo; 
    },
  },
  methods: {
    insert: function(){
      this.api_post_memo(this.title, this.content);
      this.form_reset();
    },
    modify: function(item){
      this.modify_flg = true;
      this.title = item.title;
      this.content = item.content;
      this.modify_memo = item;
    },
    modify_execute: function(){
      var memo_data = this.modify_memo;
      memo_data.title = this.title;
      memo_data.content = this.content;
      this.$store.commit('memo/modify', memo_data);
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
    remove: function(item){
      if(this.modify_flg && this.modify_memo.id === item.id){
        alert("現在編集中のメモは削除できません。");
        return;
      }
      this.$store.commit('memo/remove', item);
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
    api_post_memo: async function(title, content){
      const response = await this.$axios.post('http://localhost:8000/api/v1/memo/insert',
      {
        "title": title,
        "content": content,
      });
      console.log(response);
      this.api_get_memos();
    },
    api_get_memos: async function(){
      const response = await this.$axios.get('http://localhost:8000/api/v1/memo');
      this.memo_list = response.data;
    }
  },
  created: function(){
    console.log('created');
    this.api_get_memos();
    //this.memo_list = this.api_get_memos();
    //IDのリセット
    //this.$store.commit('memo/set_latest_id');
    //this.$store.commit('memo/set_page',0);
    //メモを全消ししたいときに有効にすればいい
    //this.$store.commit('memo/memo_list',[]);
  },
}
</script>