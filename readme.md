# 简介
抓取最新的无锡水务公众号中的水费信息（默认8小时更新一次数据）

数据源地址： https://wechat.wxwater.com.cn

# 安装
手动安装，放入 <config directory>/custom_components/ 目录

# 配置
**Example configuration.yaml:**
```yaml
sensor:
  - platform: waterprice
    name: 水费余额
    region: 户号 
```


# 前台界面
前台建议使用markdown进行自定义绘制，当然你要是觉得其他卡片也挺好看的那当然也行

![avatar](https://github.com/maydaychen/WaterPrice/blob/master/1.PNG)

直接使用markdown配置：
```yaml
type: markdown
content: >
  <ha-icon icon="mdi:update"></ha-icon> {{ state_attr('sensor.shui_fei_yu_e',
  'update_time')}} 

  ##  <center>水费余额 &nbsp;  &nbsp;  &nbsp;  <font color=#34a853> {{
  states('sensor.shui_fei_yu_e') }}  </font></center> 

```