<template>

  <div id="transcription" class="row">

    <div id="loading" v-if="loading">
     <icon name="spinner" scale="2" class="fa-spin"></icon>
    </div>
    <div class="col-sm-6">
        <image-viewer :url="url" v-on:imageLoaded="onImageLoaded"></image-viewer>
     </div>
    <div class="col-sm-5">

                  <h1>{{ barcode }}</h1>
                  <form v-on:submit.prevent>
                      <transcription-form :schema="schema" :model="model" :options="formOptions"></transcription-form>
      </form>

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
  mounted: function () {
    console.log('mounted');
    this.loadSpecimen();
  },
  methods: {
      loadSpecimen: function() {
          this.loading = true;
          // this.$http.get(this.$config.api + '/not-transcribed').then(response => {
          //         console.log("Record loaded");
          //         this.url = response.body.record.url;
          //         this.barcode = response.body.record.barcode;
          //         this._id = response.body.record._id;
          //     }, response => {
          //       console.log('Fetch Failed');
          // });
      },
      saveSpecimen: function(country) {
          let data = {
              country: country.toString(),
              barcode: this.barcode,
              url: this.url,
          };
          this.$http.put(this.$config.api + '/' + this._id + '/', data).then(response => {
                  console.log('SAVED RECORD');
                  this.loadSpecimen();
              }, response => {
                console.log('Save Failed');
          });
      },
      onSubmit: function(model) {
          this.saveSpecimen(model.country);
          console.log("LOAD");
      },
      onImageLoaded: function(){
        this.loading = false;
      }
  },    
  data () {
      return {
        loading: true,
        url: 'http://www.nhm.ac.uk/services/media-store/asset/08e4e31baf6e6a1573cde76459e95311832f2644/contents/preview',
        barcode: null,
        model: {
            type_status: null
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
                type: "input",
                label: "Is it a type specimen",
                model: "Isitatypespecimen",
                inputType: "text",
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


