import axios from "axios";
import {API_ENDPOINT_URL} from "@/api/endpoints";

const ApiService = {
    /* This is a HTTP API service to serve as a base for creating
       resource-specific API services so as to reduce the amount
       of boilerplate code.
    */ 

    get(resource, slug='') {
        // Sends GET request for a resource given a slug
        return axios.get(API_ENDPOINT_URL, `${resource}/${slug}`).catch(error => {
            throw new Error(`HTTP-Service GET Error ${error}`);
        });
    },
    getAll(resource) {
        return axios.get(API_ENDPOINT_URL, `${resource}`).catch(error => {
            throw new Error(`HTTP-Service GET ALL Error ${error}`)
        });
    },
    query(resource, params) {
        // Sends GET request for a resource given params
        return axios.get(API_ENDPOINT_URL, `${resource}`, params).catch(error => {
            throw new Error(`HTTP-Service Query Error ${error}`);
        });
    },
    post(resource, params) {
        return axios.post(API_ENDPOINT_URL, `${resource}`, params).catch(error => {
            throw new Error(`HTTP-Service POST Error ${error}`);
        }); 
    },
    put(resource, slug, params) {
        // Sends a PUT request for a resource given a slug and params
        return axios.put(API_ENDPOINT_URL, `${resource}/${slug}`, params).catch(error => {
            throw new Error(`HTTP-Service PUT Error ${error}`);
        });
    },
    update(resource, params) {
        // Sends a PUT request for a resource given params
        return axios.put(API_ENDPOINT_URL, `${resource}`, params).catch(error => {
            throw new Error(`HTTP-Service UPDATE Error ${error}`);
        });
    },
    delete(resource, params) {
        return axios.delete(API_ENDPOINT_URL, `${resource}`, params).catch(error => {
            throw new Error(`HTTP-Service DELETE Error ${error}`)
        });
    }

}

export default ApiService;