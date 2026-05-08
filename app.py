import random
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="댄스학원 랜덤 자리 배정",
    page_icon="💃",
    layout="centered"
)

# -----------------------------
# 기본 자리 데이터
# x, y는 배치도 안에서의 위치(%)입니다.
# -----------------------------
SEATS = [
    {"id": "A1", "x": 9.5, "y": 28},
    {"id": "A2", "x": 28, "y": 28},
    {"id": "A3", "x": 75.5, "y": 25.5},
    {"id": "A4", "x": 68.8, "y": 37},
    {"id": "A5", "x": 4, "y": 46},
    {"id": "A6", "x": 22, "y": 46},
    {"id": "A7", "x": 40.5, "y": 45.5},
    {"id": "A8", "x": 62.5, "y": 58},
    {"id": "A9", "x": 90.5, "y": 58},
    {"id": "A10", "x": 44.5, "y": 66.5},
    {"id": "A11", "x": 9.7, "y": 76},
    {"id": "A12", "x": 28, "y": 76},
    {"id": "A13", "x": 50, "y": 84},
    {"id": "A14", "x": 71, "y": 84},
    {"id": "A15", "x": 87.5, "y": 84},
]

DEFAULT_MEMBERS = """영미
경아
유정
우진
섬결
소현
승희
금순
윤설
인희
미정
용민
영숙
보라
금랑"""

if "assignments" not in st.session_state:
    st.session_state.assignments = {}

if "members_text" not in st.session_state:
    st.session_state.members_text = DEFAULT_MEMBERS


# -----------------------------
# 함수
# -----------------------------
def parse_names(text):
    names = []
    for line in text.splitlines():
        name = line.strip()
        if name:
            names.append(name)
    return names


def random_assign(names):
    names = names[:15]

    # 소현 / 미정 금지 자리
    forbidden_front_seats = ["A1", "A2", "A3"]

    # 우진 & 금순 앞뒤 금지 자리
    front_back_pairs = [
        ("A1", "A5"),
        ("A2", "A6"),
        ("A3", "A4"),
        ("A4", "A8"),
        ("A5", "A11"),
        ("A6", "A12"),
        ("A7", "A10"),
        ("A10", "A13"),
        ("A13", "A14"),
        ("A14", "A15")
    ]

    while True:
        seat_ids = [seat["id"] for seat in SEATS]
        random.shuffle(names)
        random.shuffle(seat_ids)

        assignments = dict(zip(seat_ids, names))

        # 소현 / 미정 자리 체크
        forbidden_members = ["소현", "미정"]

        invalid = False

        for seat, name in assignments.items():
            if name in forbidden_members and seat in forbidden_front_seats:
                invalid = True
                break

        if invalid:
            continue

        # 우진 & 금순 앞뒤 체크
        woojin_seat = None
        geumsun_seat = None

        for seat, name in assignments.items():
            if name == "우진":
                woojin_seat = seat
            elif name == "금순":
                geumsun_seat = seat

        is_adjacent = False
        for a, b in front_back_pairs:
            if (
                (woojin_seat == a and geumsun_seat == b) or
                (woojin_seat == b and geumsun_seat == a)
            ):
                is_adjacent = True
                break

        if is_adjacent:
            continue

        return assignments


def current_assign():
    # 사용자가 올려준 현재 자리 기준
    return {
        "A1": "영미",
        "A2": "경아",
        "A3": "유정",
        "A4": "우진",
        "A5": "섬결",
        "A6": "소현",
        "A7": "승희",
        "A8": "금순",
        "A9": "윤설",
        "A10": "인희",
        "A11": "미정",
        "A12": "용민",
        "A13": "영숙",
        "A14": "보라",
        "A15": "금랑",
    }


def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None


def make_studio_html(assignments):
    # 같은 폴더에 layout.png 파일을 넣으면, 사용자가 준 배치도 이미지를 배경으로 사용합니다.
    bg = image_to_base64("layout.png")

    seat_html = ""
    for seat in SEATS:
        seat_id = seat["id"]
        name = assignments.get(seat_id, "")
        if name:
            seat_html += f"""
            <div class='seat' style='left:{seat['x']}%; top:{seat['y']}%;'>
                {name}
            </div>
            """

    if bg:
        background_css = f"""
            background-image: url('data:image/png;base64,{bg}');
            background-size: 100% 100%;
            background-repeat: no-repeat;
            background-position: center;
        """
    else:
        background_css = """
            background: #ffffff;
            background-image:
                radial-gradient(#b8b8b8 0.7px, transparent 0.7px),
                linear-gradient(to right, rgba(10,37,64,0.45) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(10,37,64,0.45) 1px, transparent 1px);
            background-size: 12px 12px, 12.5% 25%, 12.5% 25%;
        """

    return f"""
    <style>
        .studio-wrap {{
            width: 100%;
            max-width: 760px;
            margin: 0 auto;
        }}
        .studio {{
            position: relative;
            width: 100%;
            aspect-ratio: 844 / 461;
            border: 2px solid #0a2540;
            border-radius: 12px;
            overflow: hidden;
            {background_css}
        }}
        .seat {{
            position: absolute;
            transform: translate(-50%, -50%);
            width: 10.5%;
            aspect-ratio: 1;
            border-radius: 50%;
            background: rgba(0,0,0,0.95);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-size: clamp(9px, 2.7vw, 15px);
            font-weight: 800;
            line-height: 1.15;
            word-break: keep-all;
            box-shadow: 0 2px 6px rgba(0,0,0,.25);
        }}
    </style>

    <div class='studio-wrap'>
        <div class='studio'>
            {seat_html}
        </div>
    </div>
    """


def result_text(assignments):
    lines = []
    for seat in SEATS:
        seat_id = seat["id"]
        name = assignments.get(seat_id, "")
        if name:
            lines.append(f"{seat_id} - {name}")
    return "\n".join(lines)


# -----------------------------
# 화면
# -----------------------------
st.title("🎉 이벤트 자리배정")
st.caption("이벤트용 랜덤 자리배정 프로그램입니다 😊")

with st.expander("회원 이름 입력", expanded=True):
    st.session_state.members_text = st.text_area(
        "회원 이름을 한 줄에 한 명씩 입력하세요.",
        value=st.session_state.members_text,
        height=220,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎉 이벤트 자리배정", use_container_width=True):
            names = parse_names(st.session_state.members_text)
            if not names:
                st.warning("회원 이름을 입력해주세요.")
            else:
                st.session_state.assignments = random_assign(names)
                st.success("랜덤 배정 완료!")

    with col2:
        if st.button("📍 현재 자리 불러오기", use_container_width=True):
            st.session_state.assignments = current_assign()
            st.success("현재 자리로 불러왔습니다.")

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🔄 자리 초기화", use_container_width=True):
            st.session_state.assignments = {}
            st.info("자리를 초기화했습니다.")

    with col4:
        if st.button("🗑 이름 초기화", use_container_width=True):
            st.session_state.members_text = ""
            st.session_state.assignments = {}
            st.experimental_rerun()

st.markdown("### 배치도")
components.html(make_studio_html(st.session_state.assignments), height=430, scrolling=False)

st.markdown("### 배정 결과")
if st.session_state.assignments:
    sorted_result = []
    for seat in SEATS:
        seat_id = seat["id"]
        if seat_id in st.session_state.assignments:
            sorted_result.append({"자리": seat_id, "이름": st.session_state.assignments[seat_id]})

    st.dataframe(sorted_result, use_container_width=True)

    st.text_area(
        "복사용 결과",
        value=result_text(st.session_state.assignments),
        height=180,
    )
else:
    st.info("아직 배정된 자리가 없습니다. 랜덤 배정 또는 현재 자리 불러오기를 눌러주세요.")

st.caption("※ 15명 초과 입력 시 앞 15명만 배정됩니다. 관장님 자리는 배정 대상에서 제외됩니다.")
