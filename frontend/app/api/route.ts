import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

const config = {
    headers: {
        'content-type': 'application/json'
    }
};

export const createRule = async ( name: string, rule: string) => {
    return await axios.post(`${API_URL}/create_rule`, { rule, name }, config)
        .then((response) => response.data)
        .catch((error) => {
            if (axios.isAxiosError(error)) {
                console.error(error.response?.data.detail);
                throw new Error(error.response?.data?.detail);
            } else {
                console.error('Unknown error creating rules:', error);
                throw new Error(error);
            }
        });
};

export const combineRules = async (rules: string[], operator: string) => {
    return axios.post(`${API_URL}/combine_rules`, { rules, operator}, config)
        .then((response) => response.data)
        .catch((error) => {
            if (axios.isAxiosError(error)) {
                console.error(error.response?.data.detail);
                throw new Error(error.response?.data?.detail);
            } else {
                console.error('Unknown error combining rules:', error);
                throw new Error(error);
            }
        });
};
export const evaluateRule = async (ruleName: string, data: Record<string, string>) => {
    return axios.post(`${API_URL}/evaluate_rule`, { rule_name: ruleName, data }, config)
        .then((response) => response.data)
        .catch((error) => {
            if (axios.isAxiosError(error)) {
                console.error(error.response?.data.detail);
                throw new Error(error.response?.data?.detail);
            } else {
                console.error('Unknown error evaluating rules:', error);
                throw new Error(error);
            }
        });
};

export const modifyRule = async (ruleName: string, rule: string) => {
    return axios.post(`${API_URL}/modify_rule`, { rule, name: ruleName }, config)
        .then((response) => response.data)
        .catch((error) => {
            if (axios.isAxiosError(error)) {
                console.error(error.response?.data.detail);
                throw new Error(error.response?.data?.detail);
            } else {
                console.error('Unknown error modifying rules:', error);
                throw new Error(error);
            }
        });
};

export const deleteRule = async (ruleName: string) => {
    return axios.delete(`${API_URL}/delete_rule?rule_name=${ruleName}`)
        .then((response) => response.data)
        .catch((error) => {
            if (axios.isAxiosError(error)) {
                console.error(error.response?.data.detail);
                throw new Error(error.response?.data?.detail);
            } else {
                console.error('Unknown error deleting rules:', error);
                throw new Error(error);
            }
        });
}
export const getRule = async (ruleName: string) => {
    return axios.get(`${API_URL}/get_rule?rule_name=${ruleName}`)
        .then((response) => response.data)
        .catch((error) => {
            if (axios.isAxiosError(error)) {
                console.error(error.response?.data.detail);
                throw new Error(error.response?.data?.detail);
            } else {
                console.error('Unknown error fetching rule:', error);
                throw new Error(error);
            }
        });
}

export const getAllRuleNames = async () => {
    return axios.get(`${API_URL}/get_all_rule_names`)
        .then((response) => response.data)
        .catch((error) => {
            if (axios.isAxiosError(error)) {
                console.error(error.response?.data.detail);
                throw new Error(error.response?.data?.detail);
            } else {
                console.error('Unknown error fetching rules:', error);
                throw new Error(error);
            }
        });
}

export const getCatalog = async () => {
    return axios.get(`${API_URL}/get_catalog`)
        .then((response) => response.data)
        .catch((error) => {
            if (axios.isAxiosError(error)) {
                console.error(error.response?.data.detail);
                throw new Error(error.response?.data?.detail);
            } else {
                console.error('Unknown error fetching catalog:', error);
                throw new Error(error);
            }
        });
}