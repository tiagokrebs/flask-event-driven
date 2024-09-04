Feature: Authentication

      # To do: Register first then login
      #Scenario: Successful login
      #  Given I am a user with username "test" and password "test"
      #  When I login
      #  Then I should see a success message

      Scenario: Unsuccessful login
        Given I am a user with username "wrong" and password "wrong"
        When I login
        Then I should see an error message