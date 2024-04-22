# from bioimageio_chatbot.utils import ChatbotExtension
from schema_agents import schema_tool
import pandas as pd
import asyncio

from pydantic import Field
from hypha_store import HyphaDataStore
from imjoy_rpc.hypha import connect_to_server, login
from code_interpreter import execute_code


class MalariaExplorer:
    def __init__(self, store, data_path):
        self.store = store
        resource_items = pd.read_csv(data_path).to_dict(orient="records")
        # resource_item_stats = f"""- keys: {list(resource_items[0].keys())}\n- resource types: {types}\n- Exampletags: {tags}\n""" #Here is an example: {resource_items[0]}
        self.patient_stats = f"""`Each data sample has the following keys: {list(resource_items[0].keys())}\n where 'image_data' is the path to the numpy array of the microscopy image patches of malaria parasites, its shape format is (N, channel, width, height), for example: (2000, 4, 31, 31), meaning it consists of 2000 patches of 31x31 parasite images, each image has 4 channels.""" #Here is an example: {resource_items[0]}
        self.resource_items = resource_items
        self.tools = {
            "search": lambda kwargs: self.search(**kwargs)
        }

    def get_schema(self):
        search_schema = schema_tool(self.search).input_model.schema()
        search_schema['description'] = search_schema['description'].format(patient_stats=self.patient_stats)
        return {
            "search": search_schema
        }
    
    async def search(self,
            script: str = Field(..., description="""Executable python script running in a Jupyter notebook for generating context for anwsering user query. The script can access data through the 'data' local variable which is a list of dictionaries, each dictionary contains information about one patient.""")
        ):
        """Search the Malaria Dataset for statistical information by executing Python3 script to analyze the data. You can for example, use numpy to load images and use maptlotlib to plot the age distribution.
        {patient_stats}
        """
        # load the data
        # resource_items = pd.read_csv(self.data_path).to_dict(orient="records")
        result = await execute_code(self.store, script, {"data": self.resource_items})
        return result



async def main():
    server_url = "https://chat.bioimage.io"
    token = await login({"server_url": server_url})
    server = await connect_to_server({"server_url": server_url, "token": token})
    store = HyphaDataStore()
    await store.setup(server)

    malaria_exp = MalariaExplorer(store=store, data_path="complete_patient_data.csv")
    # test the search function
    malaria_exp.get_schema()
    malaria_exp.search(script="print(data[0])")

    chatbot_extension = {
        "id": "malaria",
        "type": "bioimageio-chatbot-extension",
        "name": "Malaria Data Explorer",
        "description": "This tool will explore the malaria data by running python scripts in a Jupyter notebook. Note: User won't see the jupyter notebook outputs, to respond to the user, you must render results as markdown. In case of error, try to resolve it and run again.",
        "get_schema": malaria_exp.get_schema,
        "tools": malaria_exp.tools
    }
    chatbot_extension['config'] = {"visibility": "public"}
    svc = await server.register_service(chatbot_extension)
    print(f"Extension service registered with id: {svc.id}, you can visit the service at: https://bioimage.io/chat?server={server_url}&extension={svc.id}&assistant=Skyler")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()