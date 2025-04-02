import streamlit as st
import pandas as pd

class EisenhowerMatrix:
    def __init__(self, tasks):
        self.tasks = tasks
        
    def display(self):
        # Create a 2x2 grid for the matrix
        col1, col2 = st.columns(2)
        
        # Urgent & Important (Do)
        with col1:
            with st.expander("Urgent & Important (Do)", expanded=True):
                self._display_quadrant('urgent_important', "red")
        
        # Not Urgent & Important (Schedule)
        with col2:
            with st.expander("Not Urgent & Important (Schedule)", expanded=True):
                self._display_quadrant('not_urgent_important', "orange")
        
        # Urgent & Not Important (Delegate)
        with col1:
            with st.expander("Urgent & Not Important (Delegate)", expanded=True):
                self._display_quadrant('urgent_not_important', "blue")
        
        # Not Urgent & Not Important (Eliminate)
        with col2:
            with st.expander("Not Urgent & Not Important (Eliminate)", expanded=True):
                self._display_quadrant('not_urgent_not_important', "green")
    
    def _display_quadrant(self, quadrant_key, color):
        # Display existing tasks in this quadrant
        if self.tasks[quadrant_key]:
            for i, task in enumerate(self.tasks[quadrant_key]):
                cols = st.columns([8, 1, 1])
                
                # Task details
                with cols[0]:
                    st.markdown(f"**{task['title']}**")
                    if 'description' in task and task['description']:
                        st.write(task['description'])
                    if 'due_date' in task and task['due_date']:
                        st.write(f"Due: {task['due_date']}")
                
                # Edit button
                with cols[1]:
                    if st.button("Edit", key=f"edit_{quadrant_key}_{i}"):
                        st.session_state.editing_task = {
                            'quadrant': quadrant_key,
                            'index': i,
                            'task': task
                        }
                
                # Delete button
                with cols[2]:
                    if st.button("Delete", key=f"delete_{quadrant_key}_{i}"):
                        self.tasks[quadrant_key].pop(i)
                        st.rerun()
                
                st.divider()
        
        # Add new task form
        with st.form(key=f"add_task_{quadrant_key}"):
            st.subheader("Add New Task")
            title = st.text_input("Task Title", key=f"title_{quadrant_key}")
            description = st.text_area("Description (optional)", key=f"desc_{quadrant_key}")
            due_date = st.date_input("Due Date (optional)", key=f"date_{quadrant_key}")
            
            submit = st.form_submit_button("Add Task")
            if submit and title:
                self.tasks[quadrant_key].append({
                    'title': title,
                    'description': description,
                    'due_date': due_date.strftime('%Y-%m-%d') if due_date else None
                })
                st.rerun()
        
        # Handle editing task if applicable
        if 'editing_task' in st.session_state and st.session_state.editing_task['quadrant'] == quadrant_key:
            task = st.session_state.editing_task['task']
            index = st.session_state.editing_task['index']
            
            with st.form(key=f"edit_task_{quadrant_key}_{index}"):
                st.subheader("Edit Task")
                new_title = st.text_input("Task Title", value=task['title'])
                new_description = st.text_area("Description", value=task.get('description', ''))
                new_due_date = st.date_input("Due Date", value=pd.to_datetime(task['due_date']) if task.get('due_date') else None)
                
                # Dropdown to move task to another quadrant
                target_quadrant = st.selectbox(
                    "Move to quadrant",
                    [
                        'urgent_important',
                        'not_urgent_important',
                        'urgent_not_important',
                        'not_urgent_not_important'
                    ],
                    index=[
                        'urgent_important',
                        'not_urgent_important',
                        'urgent_not_important',
                        'not_urgent_not_important'
                    ].index(quadrant_key)
                )
                
                cols = st.columns(2)
                with cols[0]:
                    if st.form_submit_button("Save Changes"):
                        # Update task
                        updated_task = {
                            'title': new_title,
                            'description': new_description,
                            'due_date': new_due_date.strftime('%Y-%m-%d') if new_due_date else None
                        }
                        
                        # Handle moving task to a different quadrant
                        if target_quadrant != quadrant_key:
                            # Remove from current quadrant
                            self.tasks[quadrant_key].pop(index)
                            # Add to target quadrant
                            self.tasks[target_quadrant].append(updated_task)
                        else:
                            # Update in place
                            self.tasks[quadrant_key][index] = updated_task
                        
                        # Clear editing state
                        del st.session_state.editing_task
                        st.rerun()
                
                with cols[1]:
                    if st.form_submit_button("Cancel"):
                        del st.session_state.editing_task
                        st.rerun()
    
    @staticmethod
    def add_emails_as_tasks(emails):
        # Default to urgent_important quadrant for new email tasks
        quadrant = 'urgent_important'
        
        for email in emails:
            new_task = {
                'title': email['subject'],
                'description': f"From: {email['sender']}\n\n{email.get('snippet', '')}",
                'due_date': None,
                'email_id': email.get('id')
            }
            
            st.session_state.tasks[quadrant].append(new_task) 