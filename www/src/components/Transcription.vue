<template>

  <div id="transcription">     

    <div class="row">

      <div id="loading" v-show="loading">
       <icon name="spinner" scale="2" class="fa-spin"></icon>
      </div>  

       <div class="col-sm-7">
        <image-viewer :url="multimediaURL" v-on:imageLoaded="onImageLoaded"></image-viewer> 
      </div>        

      
      <div class="col-sm-5"> 
          <h1>{{ model.subject_id }}</h1>
  
          <div class="alert alert-danger" v-show="errorMessage">
            <p><strong>Error!</strong> {{ errorMessage }}</p>
          </div>  

          <form v-on:submit.prevent>
            <transcription-form :schema="schema" :model="model" :options="formOptions"></transcription-form>
          </form>

      </div>   

    </div>
  

    <div class="row-progress">
        <div class="progress">
          <div class="progress-bar progress-bar-striped progress-bar-success" role="progressbar" v-bind:style="{ width: progressBarWidth + '%' }">{{ stats.validated}} / {{ stats.total }} <strong>({{ percentageComplete }}%)</strong></div>          
        </div>    
    </div>   

  
</div>


</template>

<script>

import VueFormGenerator from "vue-form-generator";
import ImageViewer from './ImageViewer.vue'

export default {
  name: 'Transcription',
  components: {
      "transcription-form": VueFormGenerator.component,
      ImageViewer
  },  
  created: function () {
    console.log('mounted');
    this.loadSpecimen();
  },
  methods: {
      loadSpecimen: function() {
          this.loading = true;
          this.$http.get(this.$config.api).then((response) => {
            for (var i in this.model){
              this.model[i] = response.data.transcription[i]
            }
            this.stats = response.data.stats
            this.multimedia = response.data.multimedia
            this.loading = false;
          }, (response) => {
            console.log('Fetch Failed');
            console.log('ERROR:' + response);
            this.errorMessage = 'Sorry, there was an error loading the transcription. Please refresh the page.'
            }          
          )
          this.loading = true;

      },
      saveSpecimen: function() {
          this.loading = true;
          let data = {};
          for (var i in this.model){
              data[i] = this.model[i] 
              this.model[i] = null         
          }

          this.$http.post(this.$config.api, data).then(response => {
                  console.log('SAVED RECORD');
                  this.loadSpecimen();
              }, response => {
                this.errorMessage = 'Sorry, there was an error saving this transcription.'
                console.log('Save Failed:' + response);
                this.loading = false;
          });
      },
      onSubmit: function() {
          this.saveSpecimen();
          console.log("LOAD");
      },
      onImageLoaded: function(){
        this.loading = false;
      }
  },
  computed: {
    percentageComplete: function () {
      return this._.round(this.stats.validated / this.stats.total, 3) * 100
    },
    progressBarWidth: function () {
      // Needs at least 12% to show the stats text
      return this.percentageComplete + 12
    },
    multimediaURL: function () {
      // Needs at least 10% to show the stats
      return '/specimens/' + this.multimedia
    }      
  },      
  data () {
      return {
        loading: true,
        errorMessage: null,
        multimedia: null,
        stats: {},
        model: {
            type_status: null,
            subject_id : null,
            combidate : null,
            endcombidate : null,
            country : null,
            collector1 : null,
            collector2 : null,
            host_insect : null,
            host_plant : null,
            registration_number : null,
            is_type : null,
            subject_catalogue_irn : null,
            note : null,
        },
        schema: {
          groups: [
            {
              fields: [
                {
                  type: "input",
                  label: "Combidate",
                  model: "combidate",
                  inputType: "text",
                },   
                {
                  type: "input",
                  label: "End combidate",
                  model: "end_combidate",
                  inputType: "text",
                },
                {
                  type: "input",
                  label: "Country",
                  model: "country",
                  inputType: "text",
                }, 
                {
                  type: "input",
                  label: "Collector1",
                  model: "collector1",
                  inputType: "text",
                },    
                
                {
                  type: "input",
                  label: "Collector2",
                  model: "collector2",
                  inputType: "text",
                },                                 
                {
                  type: "input",
                  label: "Host Insect",
                  model: "host_insect",
                  inputType: "text",
                },         
                {
                  type: "input",
                  label: "Host Plant",
                  model: "host_plant",
                  inputType: "text",
                },          

              ]
            },
            {
              fields: [
              {
                type: "input",
                label: "Registration number",
                model: "registration_number",
                inputType: "text",
              },           

              {
                type: "radios",
                label: "Is it a type specimen?",
                model: "is_type",
                values: [
                    {name: "Yes", value:"Type"},
                    {name: "No", value:"NON-TYPE"},
                ]
              },                
              {
                type: "select",
                label: "Type status",
                model: "type_status",
                // required: true,
                // validator: VueFormGenerator.validators.required,
                values: [
                 'Holotype',
                 'Lectotype',
                 'Syntype',
                 'Paratype',
                 'Paralectotype',
                 'Type',
                 'Non-Type',
                ]
              },    
              {
                type: "input",
                label: "Subject Catalogue IRN",
                model: "subject_catalogue_irn",
                inputType: "text",
              },                      
    
              {
                type: "TextArea",
                label: "Note",
                model: "note",
                rows: 6,
              },           

              {
                  "type": "submit",
                  validateBeforeSubmit: true,
                  buttonText: "Submit",
                  onSubmit:this.onSubmit,
              }              
              ]
            }            

          ],

        } ,
        formOptions: {
            validateAfterChanged: true,
        }        
      }
  },

}
</script>


