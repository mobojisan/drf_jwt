<template>
  <div id="login-page">
    <GlobalHeader />
    <GlobalMessage />

    <!-- main area -->
    <main class="container mt-5 p-5">
      <p class="h5 mb-5">ログイン</p>
      <b-form v-on:submit.prevent="submitLogin">
        <div class="row form-group">
          <label class="col-sm-3 col-form-label">ユーザー名</label>
          <div class="col-sm-8">
            <b-input type="text" v-model="form.username" required />
          </div>
        </div>
        <div class="row form-group">
          <label class="col-sm-3 col-form-label">パスワード</label>
          <div class="col-sm-8">
            <b-input type="password" v-model="form.password" required />
          </div>
        </div>
        <div class="row text-center mt-5">
          <div class="col-sm-12">
            <b-button type="submit" variant="primary">ログイン</b-button>
          </div>
        </div>
      </b-form>
    </main>

    <!-- debug output -->
    <div class="m-5">
      <pre>form: {{ form }}</pre>
      <pre>state: {{ this.$store.state }}</pre>
    </div>
  </div>
</template>

<script>
import GlobalHeader from "@/components/GlobalHeader.vue";
import GlobalMessage from "@/components/GlobalMessage.vue";

export default {
  components: {
    GlobalHeader,
    GlobalMessage
  },
  data() {
    return {
      form: {
        username: "",
        password: ""
      }
    };
  },
  methods: {
    submitLogin: function() {
      this.$store
        .dispatch("auth/login", {
          username: this.form.username,
          password: this.form.password
        })
        .then(() => {
          console.log("Login succeeded.");
          this.$store.dispatch("message/setInfoMessage", {
            message: "ログインしました。"
          });
          // go home
          const next = this.$route.query.next || "/";
          this.$router.replace(next);
        });
    }
  }
};
</script>
