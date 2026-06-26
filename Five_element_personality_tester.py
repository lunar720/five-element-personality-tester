import streamlit as st
from math import sqrt
import pandas as pd
import plotly.express as px
from datetime import datetime
import json

st.set_page_config(page_title="五行人格测试仪", page_icon="⭐", layout="wide")

QUESTIONS = [
    {"text": "你做事果断，追求效率？", "dimension": "metal", "weight": 1.0},
    {"text": "你注重规则和秩序？", "dimension": "metal", "weight": 1.0},
    {"text": "你善于分析和判断？", "dimension": "metal", "weight": 1.2},
    {"text": "你有很强的原则性？", "dimension": "metal", "weight": 0.8},
    {"text": "你喜欢生长和发展？", "dimension": "wood", "weight": 1.0},
    {"text": "你富有同情心和仁爱？", "dimension": "wood", "weight": 1.0},
    {"text": "你善于规划和开拓？", "dimension": "wood", "weight": 1.2},
    {"text": "你重视教育和成长？", "dimension": "wood", "weight": 0.8},
    {"text": "你处事灵活，适应力强？", "dimension": "water", "weight": 1.0},
    {"text": "你善于思考和谋略？", "dimension": "water", "weight": 1.0},
    {"text": "你喜欢随遇而安？", "dimension": "water", "weight": 1.2},
    {"text": "你情感丰富细腻？", "dimension": "water", "weight": 0.8},
    {"text": "你热情洋溢，行动力强？", "dimension": "fire", "weight": 1.0},
    {"text": "你善于表达和社交？", "dimension": "fire", "weight": 1.0},
    {"text": "你喜欢创新和挑战？", "dimension": "fire", "weight": 1.2},
    {"text": "你充满活力和激情？", "dimension": "fire", "weight": 0.8},
    {"text": "你稳重踏实，值得信赖？", "dimension": "earth", "weight": 1.0},
    {"text": "你重视家庭和安全？", "dimension": "earth", "weight": 1.0},
    {"text": "你有很强的包容心？", "dimension": "earth", "weight": 1.2},
    {"text": "你注重实际和实用？", "dimension": "earth", "weight": 0.8},
]

ELEMENT_TYPES = {
    "⚔️ 金锋游侠": {
        "coords": {"metal": 8, "wood": 3, "water": 4, "fire": 3, "earth": 4},
        "desc": "刚毅果断，追求卓越。你如黄金般坚韧，有强烈的原则性和判断力，是团队中的决策者和领导者。",
        "strength": "果断理性、目标明确、执行力强",
        "weakness": "过于严肃、缺乏变通、追求完美",
        "advice": "学会宽容和接纳差异，刚柔并济会让你更具领导力。",
        "color": "#ffd700",
        "symbol": "⚔️",
        "planet": "金星",
        "direction": "西方"
    },
    "🌲 木林贤君": {
        "coords": {"metal": 3, "wood": 8, "water": 5, "fire": 4, "earth": 4},
        "desc": "仁爱包容，茁壮成长。你如参天大树般生机勃勃，富有同情心和开拓精神，是团队中的建设者和导师。",
        "strength": "仁爱善良、积极向上、善于规划",
        "weakness": "过于理想、缺乏决断、容易犹豫",
        "advice": "学会在关键时刻做出决断，坚定信念会让你的理想更有力量。",
        "color": "#4a904a",
        "symbol": "🌲",
        "planet": "木星",
        "direction": "东方"
    },
    "💧 水澜谋者": {
        "coords": {"metal": 4, "wood": 4, "water": 8, "fire": 2, "earth": 4},
        "desc": "智慧深邃，灵活多变。你如江海般包容万物，善于思考和谋略，是团队中的智囊和参谋。",
        "strength": "智慧深沉、适应力强、善于变通",
        "weakness": "过于圆滑、缺乏主见、情绪波动",
        "advice": "学会坚持自己的立场，坚定的信念会让你的智慧更有价值。",
        "color": "#4488ff",
        "symbol": "💧",
        "planet": "水星",
        "direction": "北方"
    },
    "🔥 火焰骁士": {
        "coords": {"metal": 4, "wood": 5, "water": 2, "fire": 8, "earth": 3},
        "desc": "热情奔放，光芒四射。你如火焰般炽热，充满活力和创造力，是团队中的灵魂和推动者。",
        "strength": "热情开朗、富有创造力、行动力强",
        "weakness": "过于急躁、缺乏耐心、情绪外露",
        "advice": "学会冷静思考，理性与热情的结合会让你更具魅力。",
        "color": "#ff6644",
        "symbol": "🔥",
        "planet": "火星",
        "direction": "南方"
    },
    "🌍 土岳守将": {
        "coords": {"metal": 3, "wood": 4, "water": 4, "fire": 3, "earth": 8},
        "desc": "稳重可靠，包容万物。你如大地般坚实，富有耐心和责任感，是团队中的基石和后盾。",
        "strength": "稳重踏实、富有耐心、包容大度",
        "weakness": "过于保守、缺乏变通、容易固执",
        "advice": "学会接受新事物，开放的心态会让你的包容更有价值。",
        "color": "#aa8866",
        "symbol": "🌍",
        "planet": "土星",
        "direction": "中央"
    },
}

ELEMENT_NAMES = {
    "metal": "⚔️ 金",
    "wood": "🌲 木",
    "water": "💧 水",
    "fire": "🔥 火",
    "earth": "🌍 土"
}

ELEMENT_COLORS = {
    "metal": "#ffd700",
    "wood": "#4a904a",
    "water": "#4488ff",
    "fire": "#ff6644",
    "earth": "#aa8866"
}

def calculate_element_scores(answers):
    scores = {"metal": 0, "wood": 0, "water": 0, "fire": 0, "earth": 0}
    weights = {"metal": 0, "wood": 0, "water": 0, "fire": 0, "earth": 0}
    
    for i, (q, answer) in enumerate(zip(QUESTIONS, answers)):
        dim = q["dimension"]
        scores[dim] += answer * q["weight"]
        weights[dim] += q["weight"]
    
    for dim in scores:
        if weights[dim] > 0:
            scores[dim] = (scores[dim] / weights[dim]) * 2
        else:
            scores[dim] = 5
    
    return scores

def find_best_match(scores, profiles_dict):
    best_name = None
    best_dist = float('inf')
    best_info = None
    
    user_vec = [scores["metal"], scores["wood"], scores["water"], scores["fire"], scores["earth"]]
    
    for name, info in profiles_dict.items():
        profile_vec = [info["coords"]["metal"], info["coords"]["wood"], 
                      info["coords"]["water"], info["coords"]["fire"], 
                      info["coords"]["earth"]]
        
        dist = sqrt(sum((user_vec[i] - profile_vec[i])**2 for i in range(5)))
        
        if dist < best_dist:
            best_dist = dist
            best_name = name
            best_info = info
    
    return best_name, best_info, best_dist

def save_to_history(name, scores, result_type, result_desc):
    if "history" not in st.session_state:
        st.session_state.history = []
    
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "scores": scores.copy(),
        "result_type": result_type,
        "result_desc": result_desc
    }
    st.session_state.history.append(record)
    
    if len(st.session_state.history) > 20:
        st.session_state.history = st.session_state.history[-20:]

def generate_export_data():
    if "current_result" in st.session_state and st.session_state.current_result:
        result = st.session_state.current_result
        scores = result["scores"]
        content = f"""⭐ 五行人格测试结果报告 ⭐

测试时间：{result['timestamp']}
测试者：{result['name']}

【五行属性得分】
⚔️ 金：{scores['metal']:.1f} 分
🌲 木：{scores['wood']:.1f} 分
💧 水：{scores['water']:.1f} 分
🔥 火：{scores['fire']:.1f} 分
🌍 土：{scores['earth']:.1f} 分

【匹配结果】
人格类型：{result['result_type']}
特质描述：{result['result_desc']}

⭐ 五行人格测试仪 
探索你的宇宙元素特质
"""
        return content
    elif "history" in st.session_state and st.session_state.history:
        record = st.session_state.history[-1]
        scores = record["scores"]
        content = f"""⭐ 五行人格测试结果报告 ⭐

测试时间：{record['timestamp']}
测试者：{record['name']}

【五行属性得分】
⚔️ 金：{scores['metal']:.1f} 分
🌲 木：{scores['wood']:.1f} 分
💧 水：{scores['water']:.1f} 分
🔥 火：{scores['fire']:.1f} 分
🌍 土：{scores['earth']:.1f} 分

【匹配结果】
人格类型：{record['result_type']}
特质描述：{record['result_desc']}

⭐ 五行人格测试仪 | 探索你的宇宙元素特质
"""
        return content
    else:
        return "暂无测试记录"

def render_radar_chart(scores):
    df = pd.DataFrame({
        '元素': [ELEMENT_NAMES['metal'], ELEMENT_NAMES['wood'], 
                ELEMENT_NAMES['water'], ELEMENT_NAMES['fire'], 
                ELEMENT_NAMES['earth']],
        '得分': [scores['metal'], scores['wood'], scores['water'], 
                scores['fire'], scores['earth']],
        '颜色': [ELEMENT_COLORS['metal'], ELEMENT_COLORS['wood'], 
                ELEMENT_COLORS['water'], ELEMENT_COLORS['fire'], 
                ELEMENT_COLORS['earth']]
    })
    
    fig = px.line_polar(df, r='得分', theta='元素', line_close=True,
                        range_r=[0, 10], template='plotly_dark',
                        color_discrete_sequence=[ELEMENT_COLORS[k] for k in ['metal', 'wood', 'water', 'fire', 'earth']])
    fig.update_traces(fill='toself', fillcolor='rgba(100, 100, 255, 0.2)')
    fig.update_layout(height=400, margin=dict(l=40, r=40, t=20, b=20))
    return fig

def render_result_card(result_type, result_info, best_dist, scores):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {result_info['color']}44, #1a1a2e);
                    padding: 25px; border-radius: 18px; border-left: 6px solid {result_info['color']};">
            <div style="display: flex; align-items: center; gap: 15px;">
                <span style="font-size: 3em;">{result_info['symbol']}</span>
                <div>
                    <h2 style="color: {result_info['color']}; margin: 0; font-size: 1.8em;">{result_type}</h2>
                    <p style="color: #ffd700; font-size: 1em;">对应星辰：{result_info['planet']} | 方位：{result_info['direction']}</p>
                </div>
            </div>
            <p style="font-size: 1.15em; line-height: 1.6; margin-top: 15px; color: #fff8dc;">{result_info['desc']}</p>
            <hr style="border-color: {result_info['color']}88; margin: 15px 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div style="background: {result_info['color']}33; padding: 10px; border-radius: 8px;">
                    <p style="margin: 0; color: #ffeb3b; font-size: 0.9em;">✨ 优势</p>
                    <p style="margin: 0; color: #fff8dc; font-weight: bold;">{result_info['strength']}</p>
                </div>
                <div style="background: #ff6b6b33; padding: 10px; border-radius: 8px;">
                    <p style="margin: 0; color: #ffeb3b; font-size: 0.9em;">⚠️ 可提升</p>
                    <p style="margin: 0; color: #fff8dc; font-weight: bold;">{result_info['weakness']}</p>
                </div>
            </div>
            <div style="background: #4ecdc433; padding: 12px; border-radius: 8px; margin-top: 10px;">
                <p style="margin: 0; color: #ffeb3b; font-size: 0.9em;">💡 发展建议</p>
                <p style="margin: 0; color: #fff8dc;">{result_info['advice']}</p>
            </div>
            <p style="margin-top: 15px; color: #ffd700; font-size: 0.95em;">🎯 匹配度评分：{max(0, min(100, int(100 - best_dist * 7)))}/100</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.plotly_chart(render_radar_chart(scores), use_container_width=True, key="result_card_radar")

def main():
    with st.sidebar:
        st.header("📊 功能面板")
        
        export_data = generate_export_data()
        col1, col2 = st.columns(2)
        with col1:
            copy_btn_key = "copy_btn_" + str(hash(export_data))
            if st.button("📋 复制结果", key=copy_btn_key):
                st.session_state.copied_text = export_data
                st.session_state.copy_trigger = True
            if "copy_trigger" in st.session_state and st.session_state.copy_trigger:
                st.markdown(f"""
                <script>
                navigator.clipboard.writeText({json.dumps(st.session_state.copied_text)}).then(function() {{
                    console.log('复制成功');
                }});
                </script>
                """, unsafe_allow_html=True)
                st.toast("结果已复制到剪贴板！", icon="✅")
                st.session_state.copy_trigger = False
        with col2:
            st.download_button("💾 导出结果", data=export_data, file_name="test_result.txt")
        
        st.subheader("📜 历史记录")
        if "history" in st.session_state and st.session_state.history:
            for i, record in enumerate(reversed(st.session_state.history[-5:])):
                with st.expander(f"{record['timestamp']} - {record['result_type']}"):
                    st.write(f"测试者：{record['name']}")
                    st.write(f"结果：{record['result_type']}")
                    st.write(f"得分：⚔️{record['scores']['metal']:.1f} 🌲{record['scores']['wood']:.1f} "
                            f"💧{record['scores']['water']:.1f} 🔥{record['scores']['fire']:.1f} "
                            f"🌍{record['scores']['earth']:.1f}")
            if st.button("清空历史"):
                st.session_state.history = []
                st.rerun()
        else:
            st.info("暂无历史记录")
        
        st.markdown("---")
        st.caption("⭐五行人格测试仪|基于中国传统五行理论")

    st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3e 50%, #0d0d2d 100%);
        min-height: 100vh;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2, #aa44ff); 
                padding: 35px; border-radius: 25px; text-align: center; margin-bottom: 30px;
                box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);">
        <h1 style="color: white; font-size: 2.5em; margin: 0;">⭐ 五行人格测试仪</h1>
        <p style="color: #e0e0e0; font-size: 1.2em; margin-top: 10px;">探索你的宇宙元素特质</p>
        <p style="color: #cccccc; font-size: 0.9em; margin-top: 5px;">⚔️金 · 🌲木 · 💧水 · 🔥火 · 🌍土</p>
    </div>
    """, unsafe_allow_html=True)
    
    if "page" not in st.session_state:
        st.session_state.page = "quiz"
    
    if st.session_state.page == "quiz":
        col1, col2 = st.columns([2, 1])
        with col1:
            name = st.text_input("输入你的代号：", "星际旅人")
        with col2:
            st.caption("💡 提示：每题1-5分，1=非常不符合，5=非常符合")
        
        if "answers" not in st.session_state:
            st.session_state.answers = [3] * len(QUESTIONS)
        
        st.subheader("📝 请回答下列问题")
        
        tabs = st.tabs(["⚔️ 金元素问题", "🌲 木元素问题", "💧 水元素问题", "🔥 火元素问题", "🌍 土元素问题"])
        
        for tab_idx, (tab, dim) in enumerate(zip(tabs, ["metal", "wood", "water", "fire", "earth"])):
            with tab:
                dim_questions = [(i, q) for i, q in enumerate(QUESTIONS) if q["dimension"] == dim]
                for i, q in dim_questions:
                    col_q, col_a = st.columns([3, 1])
                    with col_q:
                        st.write(f"{i+1}. {q['text']}")
                    with col_a:
                        st.session_state.answers[i] = st.slider(f"问题{i+1}", 1, 5, st.session_state.answers[i], 
                                                                key=f"q_{i}", label_visibility="collapsed")
                st.caption(f"✨ {ELEMENT_NAMES[dim]}元素题目：关注相关特质")
        
        with st.expander("📊 实时得分预览（可选）"):
            current_scores = calculate_element_scores(st.session_state.answers)
            cols = st.columns(5)
            for i, (dim, element_name) in enumerate(ELEMENT_NAMES.items()):
                cols[i].metric(element_name, f"{current_scores[dim]:.1f}", delta=None, 
                              help=f"{dim}元素得分",
                              label_visibility="visible")
        
        if st.button("✨ 开始五行匹配 ✨", type="primary", use_container_width=True):
            scores = calculate_element_scores(st.session_state.answers)
            
            match_progress = st.empty()
            match_text = st.empty()
            
            match_text.markdown("<p style='text-align: center; font-size: 1.2em; color: #ffd700;'>🔮 正在进行五行匹配...</p>", unsafe_allow_html=True)
            
            for i in range(101):
                match_progress.progress(i / 100, text=f"匹配进度：{i}%")
                import time
                time.sleep(0.01)
            
            match_text.markdown("<p style='text-align: center; font-size: 1.2em; color: #4ecdc4;'>✅ 匹配完成！</p>", unsafe_allow_html=True)
            time.sleep(0.5)
            
            match_progress.empty()
            match_text.empty()
            
            best_type, best_info, best_dist = find_best_match(scores, ELEMENT_TYPES)
            
            match_data = []
            for p_type, p_info in ELEMENT_TYPES.items():
                p_vec = [p_info["coords"]["metal"], p_info["coords"]["wood"], 
                        p_info["coords"]["water"], p_info["coords"]["fire"], 
                        p_info["coords"]["earth"]]
                user_vec = [scores["metal"], scores["wood"], scores["water"], 
                           scores["fire"], scores["earth"]]
                dist = sqrt(sum((user_vec[i] - p_vec[i])**2 for i in range(5)))
                score = max(0, min(100, int(100 - dist * 7)))
                match_data.append({"人格类型": p_type, "匹配度": f"{score}%", "距离": f"{dist:.2f}"})
            
            match_df = pd.DataFrame(match_data)
            match_df_sorted = match_df.sort_values(by="匹配度", key=lambda x: x.str.replace('%', '').astype(int), ascending=False)
            
            st.session_state.current_result = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": name,
                "scores": scores.copy(),
                "result_type": best_type,
                "result_desc": best_info["desc"],
                "best_dist": best_dist,
                "match_data": match_df_sorted.to_dict('records'),
                "best_info": best_info
            }
            
            save_to_history(name, scores, best_type, best_info["desc"])
            
            st.session_state.page = "result"
            st.rerun()
    
    elif st.session_state.page == "result":
        if "current_result" in st.session_state and st.session_state.current_result:
            result = st.session_state.current_result
            
            st.subheader("📏 各五行类型匹配度")
            st.dataframe(pd.DataFrame(result["match_data"]), use_container_width=True, hide_index=True)
            
            st.subheader("📊 你的五行属性分布")
            st.plotly_chart(render_radar_chart(result["scores"]), use_container_width=True, key="main_radar")
            
            st.subheader("✅ 匹配结果")
            render_result_card(result["result_type"], result["best_info"], result["best_dist"], result["scores"])
            
            st.balloons()
            st.toast(f"恭喜 {result['name']}！你是 {result['result_type']}！", icon="🎉")
            
            with st.expander("🔍 查看所有匹配详情"):
                st.json({
                    "name": result["name"],
                    "scores": result["scores"],
                    "matched_type": result["result_type"],
                    "confidence": max(0, min(100, int(100 - result["best_dist"] * 7))),
                    "dimensions": {
                        "metal": "⚔️ 金 - 决断力",
                        "wood": "🌲 木 - 仁爱力",
                        "water": "💧 水 - 智慧力",
                        "fire": "🔥 火 - 行动力",
                        "earth": "🌍 土 - 稳定力"
                    }
                })
            
            if st.button("🔄 重新测试", type="secondary", use_container_width=True):
                st.session_state.answers = [3] * len(QUESTIONS)
                st.session_state.current_result = None
                st.session_state.page = "quiz"
                st.rerun()

if __name__ == "__main__":
    main()
