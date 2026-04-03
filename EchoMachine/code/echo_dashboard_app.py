import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
from echo_autonomy_loop import (
    load_memories, save_memories, get_suggested_tags, log_change
)

# === FILE PATHS === #
BASE_DIR = Path("D:/Echo_Memory_Archive")
CHANGE_LOG_FILE = BASE_DIR / "memory_change_log.json"

st.set_page_config(page_title="Echo Dashboard", layout="wide")
st.title("🧠 Echo Memory Dashboard")

# === Load Memories === #
memories = load_memories()
search_term = st.text_input("🔍 Search memories:", "")

if search_term:
    filtered = [m for m in memories if search_term.lower() in m.get("text", "").lower()]
else:
    filtered = memories

# === Sidebar Actions === #
st.sidebar.header("Actions")
selected_action = st.sidebar.selectbox("Choose an action:", [
    "View + Edit Memory", "Suggest Tags", "Promote Tags", "Suggest Edit", "View Change Log"
])

# === Display Memories === #
for mem in filtered:
    with st.expander(f"📝 {mem.get('text', '')[:100]}..."):
        st.markdown(f"**Date**: {mem.get('date', 'N/A')}")
        st.markdown(f"**Tags**: {', '.join(mem.get('tags', [])) if mem.get('tags') else 'None'}")
        st.markdown(f"**Suggested Tags**: {', '.join(mem.get('suggested_tags', [])) if mem.get('suggested_tags') else 'None'}")

        if selected_action == "View + Edit Memory":
            new_text = st.text_area("Edit text:", mem.get("text", ""))
            if st.button("💾 Save", key=mem["id"] + "_save"):
                mem["text"] = new_text
                save_memories(memories)
                log_change("manual-edit", mem)
                st.success("Memory updated!")

        elif selected_action == "Suggest Tags":
            if st.button("✨ Suggest Tags", key=mem["id"] + "_suggest"):
                suggested = get_suggested_tags(mem.get("text", ""))
                mem["suggested_tags"] = suggested
                save_memories(memories)
                log_change("suggest-tags", mem)
                st.success(f"Suggested tags: {', '.join(suggested)}")

        elif selected_action == "Promote Tags":
            if st.button("📌 Promote Suggested Tags", key=mem["id"] + "_promote"):
                mem.setdefault("tags", [])
                for tag in mem.get("suggested_tags", []):
                    if tag not in mem["tags"]:
                        mem["tags"].append(tag)
                save_memories(memories)
                log_change("promote-suggested-tags", mem)
                st.success("Suggested tags promoted.")

        elif selected_action == "Suggest Edit":
            suggestion = f"Suggest clearer phrasing or tag for: '{mem.get('text', '')[:60]}...'"
            if st.button("💡 Add Edit Suggestion", key=mem["id"] + "_edit"):
                with open(BASE_DIR / "echo_suggested_edits.md", 'a', encoding='utf-8') as f:
                    f.write(f"- suggestion: {suggestion}\n  memory_id: {mem.get('id')}\n")
                log_change("suggest-edit", mem)
                st.success("Edit suggestion logged.")

# === Change Log View === #
if selected_action == "View Change Log":
    if CHANGE_LOG_FILE.exists():
        with open(CHANGE_LOG_FILE, 'r', encoding='utf-8') as f:
            log_data = json.load(f)
            for log in reversed(log_data[-30:]):  # show last 30 changes
                st.info(f"[{log['timestamp']}] {log['action']} → {log['entry'].get('text', '')[:60]}...")
    else:
        st.warning("No change log found.")
