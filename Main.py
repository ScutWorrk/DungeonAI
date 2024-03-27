import streamlit as st
import openai

#load_dotenv()
openai_api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = openai_api_key

# Initial game state
player_stats = {
    'health': 100,
    'mana': 50,
    'items': ['sword', 'shield', 'health potion', 'mana potion']
}

def generate_response(text_input):
    response = openai.chat.completion.create()
    model="gpt-3.5-turbo",
    messages=[
        {
        "role":"system",
        "content":"""
        You are a dungeon master running a text based adventure rpg with a play. 
        I'm going to have a conversation with you and you'll need to give quests, randomly make battles, and track the player stats and item. 
        Make the game short and simple. 
        Start of the game by asking me to pick between a wizard, warrior or archer, and start me off with basic items with some health potions. 
        After I pick my character, describe an interesting scenario where as an explorer I'll have goals and fight enemies along the way.
        """
        },
        {"role":"user",
        "content":text_input}
    ],   
    max_tokens=50,
    stop="\n",
    temperature=0.7
    
        
    return response.choices[0].message.content

def character_selection():
    character = st.radio("Choose your character:", ("Wizard", "Warrior", "Archer"))
    st.write("You've chosen to be a " + character + ".")
    if character == "Wizard":
        player_stats['mana'] += 20
    elif character == "Warrior":
        player_stats['health'] += 20
    elif character == "Archer":
        player_stats['items'].append('bow')
    st.write("You start with:", player_stats)

def main():
    st.title("Text Dungeon Game")

    character_selection()

    quest_prompt = "You are an explorer in a mysterious dungeon. Your goal is to find the legendary treasure hidden deep within. Along the way, you may encounter monsters and traps. Your journey begins now. What do you do?"
    
    while True:
        user_input = st.text_input("Your action:")
        quest_prompt += "\nYou: " + user_input
        response = generate_response(quest_prompt)
        st.write("Game Master:", response)
        
        # Update quest prompt with user input
        quest_prompt += "\nGame Master:" + response
        
        # Check for end game condition
        if "You found the legendary treasure!" in response:
            st.success("Congratulations! You have completed your quest!")
            break
        
        # Check for player death
        if player_stats['health'] <= 0:
            st.error("You died! Game over.")
            break

if __name__ == "__main__":
    main()
