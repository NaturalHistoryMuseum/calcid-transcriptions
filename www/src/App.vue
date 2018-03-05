<template>

  <div id="app">

    <nav class="navbar navbar-inverse fixed-top bg-inverse">
        <a class="navbar-brand" rel="home" href="" title="NHM">
            <img height="24" src="./assets/logo-white.png">
        </a>
        <a class="navbar-brand" href="#">Curator post-crowd data cleaning tool</a>
    </nav>
    <div class="container-full-width">
        <div class="row">
            <Transcription />
        </div>
    </div>

  </div>

</template>

<script>
import Transcription from './components/Transcription.vue'

export default {
  name: 'app',
  components: {
    Transcription
  }
}
</script>


<style src="./sass/app.scss" lang="scss"></style>