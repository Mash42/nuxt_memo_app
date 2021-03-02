export const state = () => ({
  memo: [],
  latest_id: 1,
})

export const mutations = {

  insert: function(state, insert_memo) {
    var d = new Date();
    var created = `${zero_padding(d.getFullYear(), 4)}-
                   ${zero_padding((d.getMonth() + 1), 2)}-
                   ${zero_padding(d.getDate(), 2)}
                   ${zero_padding(d.getHours(), 2)}:
                   ${zero_padding(d.getMinutes(), 2)}`;
    state.memo.unshift({
      id: state.latest_id,
      title: insert_memo.title,
      content: insert_memo.content,
      created: created,
    });
    state.latest_id ++;
  },
  modify: function(state, modify_memo) {
    for(var i = 0; i < state.memo.length; i++){
      let memo_data = state.memo[i];
      if(memo_data.id === modify_memo.id){
        state.memo[i] = modify_memo;
        return;
      }
    }
  },
  remove: function(state, remove_memo) {
    for (var i = 0; i < state.memo.length; i++) {
      let memo_data = state.memo[i]
      if (memo_data.id === remove_memo.id){
        state.memo.splice(i, 1);
        return;
      }
    }
  },
  memo_list: function(state, obj){
    state.memo = obj;
  },
  set_latest_id: function(state){
    state.latest_id = 1;
  },
}

//ゼロ埋め
function zero_padding(value, length){
  return ('0'.repeat(length) + value).slice(-length);
}