const urlBase = "http://192.168.0.31:5001";

/* var a = new Vue({
 *   el: admin,
 *   delimiters: ['[[', ']]'],
 *   data: {
 *     user: null,
 *     password: null,
 *     isAdmin: false
 *   },
 *   methods: {
 *     login: function() {
 *       var self = this;
 *       alert("ユーザ");
 *       if(this.user && this.password) {
 * 	axios
 * 	  .post(urlBase + "/ia",
 * 		{user: this.user,
 * 		 password: this.password}
 * 	  )
 * 	  .then(response => {
 * 	    self.isAdmin = response.data.isAdmin;
 * 	    if(self.isAdmin === true) {
 * 	      collection.$emit('ia');
 * 	      cashbook.$emit('ia');
 * 	    } else {
 * 	      alert("ユーザ名かパスワードが間違っています");
 * 	    }
 * 	  })
 * 	  .catch(error => console.log(error))
 *       } else {
 * 	alert("ユーザ名とパスワードを入力してください");
 *       }
 *     },
 *   }
 * }); */

var b = new Vue({
  el: balance,
  delimiters: ['[[', ']]'],
  data: {
    balance: 0
  },
  mounted() {
    axios
      .post(urlBase + '/gb')
      .then(response=> {
	(this.balance = response.data.balance)
      })
      .catch(error => console.log(error))
  },

  created() {
    this.$on('gb', this.getBalance)
  },

  methods: {
    getBalance: function() {
      axios
	.post(urlBase + '/gb')
	.then(response=> {
	  (this.balance = response.data.balance)
	})
	.catch(error => console.log(error))
    }
  }
});

var collection = new Vue({
  el: check,
  delimiters: ['[[', ']]'],
  data: {
    name: null,
    collection: [],
    checked: [],
    isAdmin: false
  },
  mounted() {
    var self = this;
    axios
      .post(urlBase + "/cm")
      .then(response => {
	(self.collection = response.data.ct),
	(self.checked = response.data.checked)
      })
      .catch(error => console.log(error))
  },

  created() {
    this.$on('ia', this.setPermission)
  },

  methods: {
    setPermission: function() {
      this.isAdmin = true;
    },
    inputName: function() {
      if(!this.name) {
	alert("名前を入力してください");
      } else {
	axios
	  .post(urlBase + "/am",
		{name: this.name}
	  )
	  .then(response => {
	    (this.collection = response.data.ct),
	    (this.name = "")
	  })
	  .catch(error => console.log(error))
      }
    },

    deleteMember: function(delId) {
      axios
	.post(urlBase + "/dm",
	      {id: delId}
	)
	.then(response => {
	  (this.collection = response.data.ct)
	  (b.$emit('gb'))
	})
	.catch(error => console.log(error))
    },
  },

  watch: {
    checked: function() {
      axios
	.post(urlBase + "/uc",
	      {checked: this.checked}
	).then(response => {
	  (b.$emit('gb'))
	})
	.catch(error => console.log(error))
    }
  }
});

var cashbook = new Vue({
  el: book,
  delimiters: ['[[', ']]'],
  data: {
    summary: null,
    incomes: null,
    expenses: null,
    book: [],
    isAdmin: false
  },
  mounted() {
    axios
      .post(urlBase + "/lb")
      .then(response => {
	(this.book = response.data.book)
      })
      .catch(error => console.log(error))
  },

  created() {
    this.$on('ia', this.setPermission)
  },

  methods: {
    setPermission: function() {
      this.isAdmin = true;
    },

    addAccount: function() {
      if(this.summary && (this.incomes || this.expenses)) {
	axios
	  .post(urlBase + "/aa",
		{summary: this.summary,
		 incomes: this.incomes,
		 expenses: this.expenses}
	  )
	  .then(response => {
	    (this.book = response.data.book),
	    (this.summary = null),
	    (this.incomes = null),
	    (this.expenses = null),
	    (b.$emit('gb'))
	  })
	  .catch(error => console.log(error))
      } else {
	alert("条件を入力してください");
      }
    },

    deleteAccount: function(aid) {
      axios
	.post(urlBase + "/da",
	      {id: aid}
	)
	.then(response => {
	  (this.book = response.data.book),
	  (b.$emit('gb'))
	})
	.catch(error => console.log(error))
    },
  }
});
