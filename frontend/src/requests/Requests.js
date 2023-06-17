class Requests {
    constructor(url, headers) {
        this._url = url
        this._headers = headers
    }

    signUp ({ email, password, username, first_name, last_name }) {
        return fetch(
            this._url + '/v1/users/',
            {
                method: 'POST',
                headers: this._headers,
                body: JSON.stringify({
                    email, password, username, first_name, last_name
                })
            }
        )
    }

    signIn ({ email, password }) {
        return fetch(
            this._url + '/v1/auth/token/',
            {
                method: 'POST',
                headers: this._headers,
                body: JSON.stringify({
                    email, password
                })
            }
        )
    }

    getUser () {
        const token = sessionStorage.getItem('token')
        const authorization = token ? { 'Authorization': `Bearer ${token}` } : {}

        return fetch(
            this._url + '/v1/users/me',
            {
                method: 'GET',
                credentials: 'include',
                headers: {
                    ...this._headers,
                    ...authorization
                }
            }
        )
    }

    updateUser({ 
        userId, 
        first_name=null, 
        last_name=null, 
        username=null, 
        password=null, 
        new_password=null 
    }) {
        const token = sessionStorage.getItem('token')
        const authorization = token ? { 'Authorization': `Bearer ${token}` } : {}
        
        let data = {};
        let dirtyData = { first_name, last_name, username, password, new_password }
        
        Object.keys(dirtyData).forEach((key) => {
            if (dirtyData[key] !== ''){
                data[key] = dirtyData[key];
            }
        })

        console.log(data);
        
        return fetch(
            this._url + `/v1/users/${userId}`,
            {
                method: 'PATCH',
                credentials: 'include',
                headers: {
                    ...this._headers,
                    ...authorization
                },
                body: JSON.stringify(data)
            }
        )
    }

    getTasks () {
        const token = sessionStorage.getItem('token')
        const authorization = token ? { 'Authorization': `Bearer ${token}` } : {}

        return fetch(
            this._url + '/v1/tasks/',
            {
                method: 'GET',
                credentials: 'include',
                headers: {
                    ...this._headers,
                    ...authorization
                }
            }
        )
    }

    getTask ({ task_id }) {
        const token = sessionStorage.getItem('token')
        const authorization = token ? { 'Authorization': `Bearer ${token}` } : {}

        return fetch(
            this._url + `/v1/tasks/${task_id}`,
            {
                method: 'GET',
                credentials: 'include',
                headers: {
                    ...this._headers,
                    ...authorization
                }
            }
        )
    }

    createTask ({ file, params, num_threads, priority, type }) {
        const token = sessionStorage.getItem('token')
        const authorization = token ? { 'Authorization': `Bearer ${token}` } : {}

        return fetch(
            this._url + '/v1/tasks/',
            {
                method: 'POST',
                credentials: 'include',
                headers: {
                    ...this._headers,
                    ...authorization
                },
                body: JSON.stringify({
                    file,
                    params,
                    num_threads,
                    priority,
                    type
                })
            }
        )
    }

    deleteTask ({ task_id }) {
        const token = sessionStorage.getItem('token')
        const authorization = token ? { 'Authorization': `Bearer ${token}` } : {}

        return fetch(
            this._url + `/v1/tasks/${task_id}`,
            {
                method: 'DELETE',
                credentials: 'include',
                headers: {
                    ...this._headers,
                    ...authorization
                },
            }
        )
    }

    executeTask ({ task_id }) {
        const token = sessionStorage.getItem('token')
        const authorization = token ? { 'Authorization': `Bearer ${token}` } : {}

        return fetch(
            this._url + `/v1/tasks/${task_id}/execute`,
            {
                method: 'POST',
                credentials: 'include',
                headers: {
                    ...this._headers,
                    ...authorization
                },
            }
        )
    }

    getOrder () {
        const token = sessionStorage.getItem('token')
        const authorization = token ? { 'Authorization': `Bearer ${token}` } : {}

        return fetch(
            this._url + '/v1/order/',
            {
                method: 'GET',
                credentials: 'include',
                headers: {
                    ...this._headers,
                    ...authorization
                }
            }
        )
    }

    getSystems () {
        const token = sessionStorage.getItem('token')
        const authorization = token ? { 'Authorization': `Bearer ${token}` } : {}

        return fetch(
            this._url + '/v1/system/',
            {
                method: 'GET',
                credentials: 'include',
                headers: {
                    ...this._headers,
                    ...authorization
                }
            }
        )
    }

    createSystem ({ host, threads }) {
        const token = sessionStorage.getItem('token')
        const authorization = token ? { 'Authorization': `Bearer ${token}` } : {}

        return fetch(
            this._url + '/v1/system/',
            {
                method: 'POST',
                credentials: 'include',
                headers: {
                    ...this._headers,
                    ...authorization
                },
                body: JSON.stringify({
                    host,
                    threads
                })
            }
        )
    }

    deleteSystem ({ systemId }) {
        const token = sessionStorage.getItem('token')
        const authorization = token ? { 'Authorization': `Bearer ${token}` } : {}

        return fetch(
            this._url + `/v1/system/${systemId}`,
            {
                method: 'DELETE',
                credentials: 'include',
                headers: {
                    ...this._headers,
                    ...authorization
                },
            }
        )
    }

    changeSystemState ({ systemId }) {
        const token = sessionStorage.getItem('token')
        const authorization = token ? { 'Authorization': `Bearer ${token}` } : {}

        return fetch(
            this._url + `/v1/system/${systemId}/state`,
            {
                method: 'POST',
                credentials: 'include',
                headers: {
                    ...this._headers,
                    ...authorization
                },
            }
        )
    }

    updateSystem ({ systemId, host, threads }) {
        const token = sessionStorage.getItem('token')
        const authorization = token ? { 'Authorization': `Bearer ${token}` } : {}

        return fetch(
            this._url + `/v1/system/${systemId}`,
            {
                method: 'PATCH',
                credentials: 'include',
                headers: {
                    ...this._headers,
                    ...authorization
                },
                body: JSON.stringify({
                    host,
                    threads
                })
            }
        )
    }

}

Requests = new Requests('http://localhost', { 'content-type': 'application/json' });
export default Requests;
