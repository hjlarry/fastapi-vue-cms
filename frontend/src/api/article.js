import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/articles',
    method: 'get',
    params
  })
}
