# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: recipe.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'recipe.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0crecipe.proto\x12\"de.benedikt_schwering.thicnd.stubs\"\x06\n\x04Null\"X\n\x13\x43reateRecipeRequest\x12\x41\n\x06recipe\x18\x01 \x01(\x0b\x32\x31.de.benedikt_schwering.thicnd.stubs.RecipeRequest\"d\n\x13UpdateRecipeRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x41\n\x06recipe\x18\x02 \x01(\x0b\x32\x31.de.benedikt_schwering.thicnd.stubs.RecipeRequest\"\x1d\n\x0fRecipeIdRequest\x12\n\n\x02id\x18\x01 \x01(\t\"\x82\x01\n\rRecipeRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12>\n\x05steps\x18\x04 \x03(\x0b\x32/.de.benedikt_schwering.thicnd.stubs.StepRequest\"\x82\x01\n\x0bStepRequest\x12^\n\x15quantifiedIngredients\x18\x01 \x03(\x0b\x32?.de.benedikt_schwering.thicnd.stubs.QuantifiedIngredientRequest\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\"C\n\x1bQuantifiedIngredientRequest\x12\x12\n\ningredient\x18\x01 \x01(\x03\x12\x10\n\x08quantity\x18\x02 \x01(\x01\"V\n\x0fRecipesResponse\x12\x43\n\x07recipes\x18\x01 \x03(\x0b\x32\x32.de.benedikt_schwering.thicnd.stubs.RecipeResponse\"\x90\x01\n\x0eRecipeResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12?\n\x05steps\x18\x05 \x03(\x0b\x32\x30.de.benedikt_schwering.thicnd.stubs.StepResponse\"\x90\x01\n\x0cStepResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12_\n\x15quantifiedIngredients\x18\x02 \x03(\x0b\x32@.de.benedikt_schwering.thicnd.stubs.QuantifiedIngredientResponse\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\"P\n\x1cQuantifiedIngredientResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\ningredient\x18\x02 \x01(\x03\x12\x10\n\x08quantity\x18\x03 \x01(\x01\"q\n\x18TotalIngredientsResponse\x12U\n\x10totalIngredients\x18\x01 \x03(\x0b\x32;.de.benedikt_schwering.thicnd.stubs.TotalIngredientResponse\"?\n\x17TotalIngredientResponse\x12\x12\n\ningredient\x18\x01 \x01(\x03\x12\x10\n\x08quantity\x18\x02 \x01(\x01\"=\n\x16\x41ssociatedTagsResponse\x12\x14\n\x0cintersection\x18\x01 \x03(\t\x12\r\n\x05union\x18\x02 \x03(\t2\xed\x06\n\rRecipeService\x12k\n\nGetRecipes\x12(.de.benedikt_schwering.thicnd.stubs.Null\x1a\x33.de.benedikt_schwering.thicnd.stubs.RecipesResponse\x12t\n\tGetRecipe\x12\x33.de.benedikt_schwering.thicnd.stubs.RecipeIdRequest\x1a\x32.de.benedikt_schwering.thicnd.stubs.RecipeResponse\x12\x88\x01\n\x13GetTotalIngredients\x12\x33.de.benedikt_schwering.thicnd.stubs.RecipeIdRequest\x1a<.de.benedikt_schwering.thicnd.stubs.TotalIngredientsResponse\x12\x84\x01\n\x11GetAssociatedTags\x12\x33.de.benedikt_schwering.thicnd.stubs.RecipeIdRequest\x1a:.de.benedikt_schwering.thicnd.stubs.AssociatedTagsResponse\x12{\n\x0c\x43reateRecipe\x12\x37.de.benedikt_schwering.thicnd.stubs.CreateRecipeRequest\x1a\x32.de.benedikt_schwering.thicnd.stubs.RecipeResponse\x12{\n\x0cUpdateRecipe\x12\x37.de.benedikt_schwering.thicnd.stubs.UpdateRecipeRequest\x1a\x32.de.benedikt_schwering.thicnd.stubs.RecipeResponse\x12m\n\x0c\x44\x65leteRecipe\x12\x33.de.benedikt_schwering.thicnd.stubs.RecipeIdRequest\x1a(.de.benedikt_schwering.thicnd.stubs.NullB&\n\"de.benedikt_schwering.thicnd.stubsP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'recipe_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\"de.benedikt_schwering.thicnd.stubsP\001'
  _globals['_NULL']._serialized_start=52
  _globals['_NULL']._serialized_end=58
  _globals['_CREATERECIPEREQUEST']._serialized_start=60
  _globals['_CREATERECIPEREQUEST']._serialized_end=148
  _globals['_UPDATERECIPEREQUEST']._serialized_start=150
  _globals['_UPDATERECIPEREQUEST']._serialized_end=250
  _globals['_RECIPEIDREQUEST']._serialized_start=252
  _globals['_RECIPEIDREQUEST']._serialized_end=281
  _globals['_RECIPEREQUEST']._serialized_start=284
  _globals['_RECIPEREQUEST']._serialized_end=414
  _globals['_STEPREQUEST']._serialized_start=417
  _globals['_STEPREQUEST']._serialized_end=547
  _globals['_QUANTIFIEDINGREDIENTREQUEST']._serialized_start=549
  _globals['_QUANTIFIEDINGREDIENTREQUEST']._serialized_end=616
  _globals['_RECIPESRESPONSE']._serialized_start=618
  _globals['_RECIPESRESPONSE']._serialized_end=704
  _globals['_RECIPERESPONSE']._serialized_start=707
  _globals['_RECIPERESPONSE']._serialized_end=851
  _globals['_STEPRESPONSE']._serialized_start=854
  _globals['_STEPRESPONSE']._serialized_end=998
  _globals['_QUANTIFIEDINGREDIENTRESPONSE']._serialized_start=1000
  _globals['_QUANTIFIEDINGREDIENTRESPONSE']._serialized_end=1080
  _globals['_TOTALINGREDIENTSRESPONSE']._serialized_start=1082
  _globals['_TOTALINGREDIENTSRESPONSE']._serialized_end=1195
  _globals['_TOTALINGREDIENTRESPONSE']._serialized_start=1197
  _globals['_TOTALINGREDIENTRESPONSE']._serialized_end=1260
  _globals['_ASSOCIATEDTAGSRESPONSE']._serialized_start=1262
  _globals['_ASSOCIATEDTAGSRESPONSE']._serialized_end=1323
  _globals['_RECIPESERVICE']._serialized_start=1326
  _globals['_RECIPESERVICE']._serialized_end=2203
# @@protoc_insertion_point(module_scope)
