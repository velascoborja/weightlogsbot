#!/usr/bin/env python3
"""
Test script to verify the reply-to-reminder feature works correctly.
This script tests the logic for detecting replies to reminder messages.
"""

class MockUpdate:
    def __init__(self, text, reply_to_message_id=None):
        self.message = MockMessage(text, reply_to_message_id)
        self.effective_user = MockUser()

class MockMessage:
    def __init__(self, text, reply_to_message_id=None):
        self.text = text
        if reply_to_message_id:
            self.reply_to_message = MockReplyMessage(reply_to_message_id)
        else:
            self.reply_to_message = None

class MockReplyMessage:
    def __init__(self, message_id):
        self.message_id = message_id

class MockUser:
    def __init__(self):
        self.id = 123456

class MockContext:
    def __init__(self, bot_data=None, user_data=None, chat_data=None):
        self.bot_data = bot_data or {}
        self.user_data = user_data or {}
        self.chat_data = chat_data or {}

def test_reply_detection():
    """Test the logic for detecting replies to reminder messages."""
    
    # Test case 1: Reply to a stored reminder message
    print("Test 1: Reply to stored reminder message")
    user_id = 123456
    reminder_message_id = 789
    
    context = MockContext(
        bot_data={
            "reminder_messages": {
                user_id: reminder_message_id
            }
        }
    )
    
    update = MockUpdate("75.5", reply_to_message_id=reminder_message_id)
    
    # Simulate the logic from numeric_listener
    is_reply_to_reminder = False
    if update.message.reply_to_message:
        reply_to_message_id = update.message.reply_to_message.message_id
        if (context.bot_data and 
            "reminder_messages" in context.bot_data and 
            user_id in context.bot_data["reminder_messages"] and
            context.bot_data["reminder_messages"][user_id] == reply_to_message_id):
            is_reply_to_reminder = True
    
    print(f"  Should detect reply to reminder: {is_reply_to_reminder}")
    assert is_reply_to_reminder == True, "Should detect reply to reminder message"
    
    # Test case 2: Reply to a different message
    print("Test 2: Reply to different message")
    update2 = MockUpdate("75.5", reply_to_message_id=999)  # Different message ID
    
    is_reply_to_reminder2 = False
    if update2.message.reply_to_message:
        reply_to_message_id = update2.message.reply_to_message.message_id
        if (context.bot_data and 
            "reminder_messages" in context.bot_data and 
            user_id in context.bot_data["reminder_messages"] and
            context.bot_data["reminder_messages"][user_id] == reply_to_message_id):
            is_reply_to_reminder2 = True
    
    print(f"  Should NOT detect reply to reminder: {is_reply_to_reminder2}")
    assert is_reply_to_reminder2 == False, "Should not detect reply to different message"
    
    # Test case 3: No reply at all
    print("Test 3: No reply message")
    update3 = MockUpdate("75.5")  # No reply
    
    is_reply_to_reminder3 = False
    if update3.message.reply_to_message:
        reply_to_message_id = update3.message.reply_to_message.message_id
        if (context.bot_data and 
            "reminder_messages" in context.bot_data and 
            user_id in context.bot_data["reminder_messages"] and
            context.bot_data["reminder_messages"][user_id] == reply_to_message_id):
            is_reply_to_reminder3 = True
    
    print(f"  Should NOT detect reply to reminder: {is_reply_to_reminder3}")
    assert is_reply_to_reminder3 == False, "Should not detect reply when no reply message"
    
    print("All tests passed! ✅")

if __name__ == "__main__":
    test_reply_detection()
