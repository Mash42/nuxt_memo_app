<template>
  <v-row>
  <v-col cols="6">
    <v-btn @click="get_users" color="primary">GET USERS</v-btn>
    <table v-if="users.length > 0">
      <th>
        <td>ID</td>
        <td>NAME</td>
      </th>
      <tr v-for="(user, index) in users" :key="index">
        <td>{{user.id}}</td>
        <td>{{user.name}}</td>
      </tr>
    </table>
  </v-col>
  </v-row>
</template>
<script>
const axios = require('axios');
export default {
  data: function(){
    return {
      users: [],
    }
  },
  methods: {
    get_users: function(){
      let self = this;
      axios.get('http://localhost:8000/api/v1/users')
      .then(function(response) {
        console.log(response.data);
        self.users = response.data;
      })
      .catch(function(error) {
        console.log('ERROR!! occurred in Backend.')
        console.log(error);
      });
    }
  }
}
</script>