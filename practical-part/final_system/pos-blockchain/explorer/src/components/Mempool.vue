<template>
  <div>
    <div class="container"><h3>Pending Transactions:</h3>  </div>
      <table>
        <thead>
        <tr>
          <th>Hash</th>
          <th>From</th>
          <th>To</th>
          <th>Amount</th>
          <th>timestamp</th>
        </tr>
        </thead>

        <tbody>
        <tr v-for="transaction in transactions">

          <td>{{ transaction.signature}}</td>
          <td><router-link :to="{ name: 'Address', params: { address: transaction.sender_public_key }}"> <span >{{ transaction.sender_public_key }}</span></router-link></td>
          <td><router-link :to="{ name: 'Address', params: { address: transaction.receiver_public_key }}"> <span >{{ transaction.receiver_public_key }}</span></router-link></td>
          <td>{{ transaction.amount}}</td>
          <td>{{ transaction.timestamp}}</td>
        </tr>
        </tbody>
      </table>
    </div>

</template>

<script>
  export default {
    name: 'Mempool',
    data() {
      return {
        transactions :[]

      }
    },
    created() {
      this.getTransactionPool();
    },
    methods: {
      getTransactionPool: function () {
        this.$http.get('http://localhost:8050/api/v1/transaction/transaction_pool/')
          .then(resp => {
            this.transactions = resp.data;
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
