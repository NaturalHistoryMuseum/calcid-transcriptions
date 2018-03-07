<template>

  <div id="app">
  
    <nav class="navbar navbar-inverse fixed-top bg-inverse">
      <div class="container-full-width">
        <a class="navbar-brand" rel="home" href="" title="NHM">
            <img height="24" src="./assets/logo-white.png">
        </a>
        <a class="navbar-brand" href="#">Curator post-crowd data cleaning tool</a>
        <a title="Download validated transcriptions as CSV" :href="downloadURL" class="navbar-right"><icon name="download" scale="2"></icon></a>
      </div>              
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
  },
  computed: {
    downloadURL: function () {
      return this.$config.api + 'export'
    },
  }      
}
</script>


<style src="./sass/app.scss" lang="scss"></style>