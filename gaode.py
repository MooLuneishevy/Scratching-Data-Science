import datetime
import requests
import codecs
import time
def gaode():
    ak=['here are your aks']
    ak_cnt=0
    # 设定网格单元的基础经纬度和宽度
    baselng,baselat=114.143639,30.477906
    widthlng,widthlat=0.013,0.012
    # 循环每个网格进行数据爬取 在这里构建了(23,20)网格
    for i in range(0,23):
        i_tmp=i
        startlat=round(baselat+i*widthlat,6)
        endlat=round(startlat+widthlat,6)
        for j in range(0,20):
            print(f"now working ({i},{j})")
            startlng=round(baselng+j*widthlng,6)
            endlng=round(startlng+widthlng,6)
            ak_idx=ak_cnt%len(ak)
            ak_use=ak[ak_idx]
            url_1="https://api.map.baidu.com/traffic/v1/polygon?ak="+ak_use+"&vertexes="
            url_2="&coord_type_input=gcj02&coord_type_output=gcj02"
            location=str(startlat)+","+str(endlng)+";"+str(endlat)+","+str(endlng)+";"+str(endlat)+","+str(startlng)+";"+str(startlat)+","+str(startlng)
            url=url_1+location+url_2
            # 爬取数据
            data=requests.get(url).json()
            ak_cnt+=1
            road_traffic=data.get('road_traffic')
            evaluation=data.get('evaluation')
            if not isinstance(road_traffic, list):
                continue
            for i1,road in enumerate(road_traffic):
                congestion_sections=road.get('congestion_sections',[])
                for i2,section in enumerate(congestion_sections):
                    # 处理拥堵段数据
                    curr_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    res=[
                        road.get('road_name'),
                        curr_time,
                        evaluation.get('status'),
                        evaluation.get('status_desc'),
                        section.get('section_desc'),
                        section.get('status'),
                        section.get('speed'),
                        section.get('congestion_distance'),
                        section.get('congestion_trend')
                    ]
                    with codecs.open("res_out.txt",'a','gbk') as f:
                        f.write(f"{i_tmp},{j},")
                        f.write(','.join(map(str, res))+'\n')
                    res.clear()
                if not congestion_sections:
                    # 如果没有拥堵段 则记录道路状态为畅通
                    curr_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    res=[road.get('road_name'),curr_time,"1","畅通"]
                    with codecs.open("res_out.txt",'a','gbk') as f:
                        f.write(f"{i_tmp},{j},")
                        f.write(','.join(map(str, res))+'\n')
                    res.clear()
            time.sleep(0.1)
def main():
    gaode()
if __name__ == "__main__":
    main()