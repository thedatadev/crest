import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
import {API_ENDPOINT_URL} from "@/api/endpoints";

const ApiService = {
    /* This is a HTTP API service to serve as a base for creating
       resource-specific API services so as to reduce the amount
       of boilerplate code.
    */ 

    init() {
        // The init() method gets invoked in src/main.js
        Vue.use(VueAxios, axios);
        Vue.axios.defaults.baseURL = API_ENDPOINT_URL;
    },
    get(resource, slug='') {
        // Sends GET request for a resource given a slug
        return Vue.axios.get(`${resource}/${slug}`).catch(error => {
            throw new Error(`HTTP-Service GET Error ${error}`);
        });
    },
    getAll(resource) {
        return Vue.axios.get(`${resource}`).catch(error => {
            throw new Error(`HTTP-Service GET ALL Error ${error}`)
        });
    },
    query(resource, params) {
        // Sends GET request for a resource given params
        return Vue.axios.get(`${resource}`, params).catch(error => {
            throw new Error(`HTTP-Service Query Error ${error}`);
        });
    },
    post(resource, params) {
        return Vue.axios.post(`${resource}`, params).catch(error => {
            throw new Error(`HTTP-Service POST Error ${error}`);
        }); 
    },
    put(resource, slug, params) {
        // Sends a PUT request for a resource given a slug and params
        return Vue.axios.put(`${resource}/${slug}`, params).catch(error => {
            throw new Error(`HTTP-Service PUT Error ${error}`);
        });
    },
    update(resource, params) {
        // Sends a PUT request for a resource given params
        return Vue.axios.put(`${resource}`, params).catch(error => {
            throw new Error(`HTTP-Service UPDATE Error ${error}`);
        });
    },
    delete(resource, params) {
        return Vue.axios.delete(`${resource}`, params).catch(error => {
            throw new Error(`HTTP-Service DELETE Error ${error}`)
        });
    }

}

export default ApiService;