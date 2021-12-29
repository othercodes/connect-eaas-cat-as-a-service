Feature: Place new purchase order for new customer

  Background: The reseller has setup the configuration successfully.
    Given asset request
    And request with product "PRODUCT_ID"
    And request with marketplace "MARKETPLACE_ID"
    And request with asset tier1 "ACCOUNT_TIER1_ID"
    And request with connection "CONNECTION_ID" of type "CONNECTION_TYPE"
    And request with parameter "Address Line 1" with value "305 Withington Ave"
    And request with parameter "City" with value "Rio Linda"
    And request with parameter "State Or Province Or Region" with value "California"
    And request with parameter "ZIP or Postal Code" with value "95673"
    And request with parameter "Country" with value "US"
    And request with parameter "Phone Number" with value " 9169926566"
    And request with item "PRD-568-313-088-0001" with mpn "MPN-CAT-IMG" x12

  Scenario:
    Given request with parameter "Order Type" with value "RANDOM"
    Given request with parameter "Categories" with value "4, 5"
    When subscription request is processed
    Then request status is "approved"
    And request parameter "Cat Subscription ID" value match "/^AS-\d{4}-\d{4}-\d{4}$/"
