Feature: Create an account in Battle.net

  Scenario: Check cookies compliance
    Given cookie compliance box appears
    When I click on Accept
    Then the box is closed

  Scenario Outline: Fill in age
    Given there is an element with id "age"
    When I fill in with <input_value>
    Then the element contains <output_value>

  Examples:
    | input_value | output_value  |
    | 0           | 0             |
    | 999         | 999           |
    | 50          | 50            |
    | 9999        | 999           |
    | a           | empty         |

  Scenario Outline: Fill in name
    Given there is an element with id "firstname"
    When I fill in with <input_value>
    Then the element contains <output_value>

  Examples:
    | input_value                       | output_value                     |
    | TestName1                         | TestName1                        |
    | TestWithMoreThan32Characters_1234 | TestWithMoreThan32Characters_123 |
    | 1234                              | 1234                             |
    | $%&                               | $%&                              |

  Scenario Outline: Fill in lastname
    Given there is an element with id "lastname"
    When I fill in with <input_value>
    Then the element contains <output_value>

  Examples:
    | input_value                       | output_value                     |
    | TestLastname1                     | TestLastname1                    |
    | TestWithMoreThan32Characters_1234 | TestWithMoreThan32Characters_123 |
    | 1234                              | 1234                             |
    | $%&                               | $%&                              |


  Scenario Outline: Fill in email
    Given there is an element with id "emailAddress"
    When I fill in with <input_value>
    And the focus is lost in that element pressing tab key
    Then there is an element with id "emailAddress-error-inline"
    And its text is <text_error>

  Examples:
    | input_value            | text_error                                         |
    | valid@email.com        | empty                                              |
    | invalid@email@.com     | Esta dirección de correo electrónico no es válida. |
    | invalid@email          | Esta dirección de correo electrónico no es válida. |
    | invalid$$@email.com    | Esta dirección de correo electrónico no es válida. |

  Scenario Outline: Fill in password
    Given there is an element with id "emailAddress"
    And I fill in with <email>
    And there is an element with id "password"
    When I fill in with <password>
    And there is an element with id "rePassword"
    And I fill in with <repassword>
    And the focus is lost in that element pressing tab key
    Then there is an element with id "password-error-inline"
    And its text is <text_error>
    And the password strength is <strength>
    And there is an element with class "popover-content"
    And its children are list elements
    And check password guideline length <A>
    And check password guideline alphanumeric value <B>
    And check password guideline special characters <C>
    And check password guideline similar to email <D>

  Examples:
    | email          | password      | repassword     | text_error                      | strength        | A             | B             | C             | D             |
    | name@gmail.com | empty         | empty          | Las contraseñas deben coincidir.| empty           | neutral       | neutral       | neutral       | neutral       |
    | name@gmail.com | test12345     | test12345      | empty                           | Aceptable       | passing muted | passing muted | passing muted | passing muted |
    | name@gmail.com | test123456789 | test123456789  | empty                           | Fuerte          | passing muted | passing muted | passing muted | passing muted |
    | name@gmail.com | hellomyfriend | hellomyfriend  | empty                           | Débil           | passing muted | failing       | passing muted | passing muted |
    | name@gmail.com | abcd1         | abcd1          | empty                           | Demasiado corta | failing       | passing muted | passing muted | passing muted |
    | name@gmail.com | españa12345   | españa12345    | empty                           | Débil           | passing muted | passing muted | failing       | passing muted |
    | name@gmail.com | namegmail1    | namegmail1     | empty                           | Fuerte          | passing muted | passing muted | passing muted | failing       |
    | name@gmail.com | test12345     | test44444      | Las contraseñas deben coincidir.| empty           | passing muted | passing muted | passing muted | passing muted |

  Scenario: blizzardNewsletter checkbox is selected and not selected
    Given there is an element with id "blizzardNewsletter"
    And class of parent is "checkbox-label"
    When I click on parent
    Then class of parent is "checkbox-label focus checked"
    And I click on parent
    And class of parent is "checkbox-label focus"
    And I click on parent
    And class of parent is "checkbox-label focus checked"

  Scenario: agreedToPrivacyPolicy checkbox is selected and not selected
    Given there is an element with id "agreedToPrivacyPolicy"
    And class of parent is "checkbox-label"
#    ToDo click on select box
#    When I click on parent
#    Then class of parent is "checkbox-label focus checked"
#    And I click on parent
#    And class of parent is "checkbox-label focus"

  Scenario: Check all links work
    When there are some links
    Then I navigate to each link and check response status code is lower than 400

 Scenario: Select Region and Language
   Given there are some regions to choose
   And there are some language to choose
   When I want to choose my region and language
   Then I check Americas and its languages
   Then I check Europe and its languages
   Then I check Corea and its languages
   Then I check Taiwan and its languages
   Then I check China and its languages
   Then I check Southeast Asia and its languages

  Scenario: Check all country list
    When I get all the options of the list
    Then HTTP GET country param is changed and current option selected is changed
    And I return to "https://eu.battle.net/account/creation/tos.html"