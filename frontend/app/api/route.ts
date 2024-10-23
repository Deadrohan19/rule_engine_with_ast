import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

const config = {
    headers: {
        'content-type': 'application/json'
    }
};

const handleApiError = (error: unknown): never => {
  if (axios.isAxiosError(error)) {
    // console.error(error.response?.data.detail);
    throw error.response?.data?.detail;
  }
  throw new Error('An unexpected error occurred');
};

export const createRule = async ( name: string, rule: string) => {
    try{
        return await axios.post(`${API_URL}/create_rule`, { rule, name }, config).then((response) => response.data)
    } catch (error) {
        handleApiError(error);
    }
};

export const combineRules = async (rules: string[], operator: 'AND' | 'OR') => {
    try{
        return axios.post(`${API_URL}/combine_rules`, { rules, operator}, config).then((response) => response.data)
    } catch (error) {
        handleApiError(error);
    }
};
export const evaluateRule = async (ruleName: string, data: Record<string, string>) => {
    try{
        return axios.post(`${API_URL}/evaluate_rule`, { rule_name: ruleName, data }, config).then((response) => response.data)
    } catch (error) {
        handleApiError(error);
    }
};

export const modifyRule = async (ruleName: string, rule: string) => {
    try{
        return axios.post(`${API_URL}/modify_rule`, { rule, name: ruleName }, config).then((response) => response.data)
    } catch (error) {
        handleApiError(error);
    }
};

export const deleteRule = async (ruleName: string) => {
    try{
        return axios.delete(`${API_URL}/delete_rule?rule_name=${ruleName}`).then((response) => response.data)
    } catch (error) {
        handleApiError(error);
    }
}
export const getRule = async (ruleName: string) => {
    try{
        return axios.get(`${API_URL}/get_rule?rule_name=${ruleName}`).then((response) => response.data)
    } catch (error) {
        handleApiError(error);
    }
}

export const getAllRuleNames = async () => {
    try{
        return axios.get(`${API_URL}/get_all_rule_names`).then((response) => response.data)
    } catch (error) {
        handleApiError(error);
    }
}

export const getCatalog = async () => {
    try{
        return axios.get(`${API_URL}/get_catalog`).then((response) => response.data)
    } catch (error) {
        handleApiError(error);
    }
}