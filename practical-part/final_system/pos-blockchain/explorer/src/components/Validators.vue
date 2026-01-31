<template>
  <div>
    <div class="container"><h3>Validators:</h3>  </div>
      <table>
        <thead>
        <tr>
          <th>Name</th>
          <th>ip</th>
          <th>Port</th>
        </tr>
        </thead>

        <tbody>
        <tr v-for="peer in peers">
          <td>{{ peer.docker_ip }}</td>
          <td>{{ peer.ip }}</td>
          <td>{{ peer.port}}</td>
        </tr>
        </tbody>
      </table>
    </div>

</template>

<script>
  export default {
    name: 'Validators',
    data() {
      return {
        peers :[]

      }
    },
    created() {
      this.getPeers();
    },
    methods: {
      getPeers: function () {
        this.$http.get('http://localhost:8050/api/v1/blockchain/peers/')
          .then(resp => {
            this.peers = resp.data;
          })
      }
    }
  }
</script>


<style scoped>
.table-container {
  width: 100%;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

th {
  background-color: #f4f4f4;
}
</style>
