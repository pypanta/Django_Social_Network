<template>
  <section class="auth">
    <div>
      <h2>Log In</h2>
      <p>Dolor veritatis iste excepturi velit delectus. Consequatur quasi nisi earum temporibus vero id harum Est perferendis at nobis animi nesciunt. Vel voluptatum odio earum similique officiis eveniet placeat.</p>
      <p>Amet magnam aperiam magnam eligendi sunt Ut eaque eius magnam fugiat maxime Assumenda sapiente iste odio perferendis libero Enim tempore quos totam laboriosam consectetur. Dignissimos eum dolores soluta cum eligendi.</p>
      <p>
        Don't have an account?
        <router-link :to="{ name: 'signup' }">
          Click here
        </router-link> to create one!
      </p>
    </div>
    <div>
      <form class="auth-form">
        <div class="auth-form-group">
          <label for="">E-mail</label>
          <input type="email" placeholder="Your e-mail address">
        </div>
        <div class="auth-form-group">
          <label for="">Password</label>
          <input type="password" placeholder="Your password">
        </div>
        <input type="submit" value="Log In" class="btn btn-success">
      </form>
    </div>
  </section>
</template>

<script setup>
</script>
