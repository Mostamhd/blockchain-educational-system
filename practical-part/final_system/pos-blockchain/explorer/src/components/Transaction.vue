<template>

  <div>
  <div class="container"><h3>Transaction: {{transaction.hash}}</h3>  </div>

    <table>
      <tbody>
      <tr>
        <td>Hash</td>
        <td><span >{{ transaction.hash }}</span></td>
      </tr>
      <tr>
        <td>From</td>
        <td v-if="transaction.sender_public_key == 'COINBASE'">{{ transaction.sender_public_key}}</td>
        <td v-else><router-link  :to="{ name: 'Address', params: { address: transaction.sender_public_key }}"> <span >{{ transaction.sender_public_key }}</span></router-link></td>
      </tr>
      <tr>
        <td>To</td>
        <td><router-link :to="{ name: 'Address', params: { address: transaction.receiver_public_key }}"> <span >{{ transaction.receiver_public_key }}</span></router-link></td>
      </tr>
      <tr>
        <td>Amount</td>
        <td>{{ transaction.amount}}</td>
      </tr>
      <tr>
        <td>Signature</td>
        <td><span >{{ transaction.signature }}</span></td>
      </tr>

      </tbody>
    </table>
  </div>
</template>

<script>
  export default {
    name: 'Transaction',
    data() {
      return {
        transaction :{}
      }
    },
    created() {
      this.getTransaction(this.$route.params.id)
    },
    update() {
      console.log('update')
    },
    methods: {
      getTransaction: function (id) {
          console.log('tsers')
        this.$http.get('http://localhost:8050/api/v1/transaction/' + id)
          .then(resp => {
            this.transaction = resp.data;
          })
      },
      trimAddress: function(address) {
        return address.substr(0,24) + '...';
      },
      totalValue: function(transaction) {
        return _(transaction.txOuts)
          .map(txOut => txOut.amount)
          .sum()
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

.transaction {
    padding: 1em;
    margin-bottom: 1em;
    background-color: gainsboro;
  }
.tx{
  max-width: 80%;
}

</style>
